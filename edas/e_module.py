__doc__ = \
'''-- Edas module for MycroPython'''
''' CheckTimeの y_wait に update指定を追加 '''
__version__ = "0.09.04"
import time
from micropython import const
from machine import Timer
import rp2

TypeGenerator = type((lambda: (yield))())

def is_generator(obj):
    ''' ジェネレータオブジェクトの判定 '''
    return isinstance(obj, TypeGenerator)

class MyTimer():
    ''' StateMachineからの割り込みを使ったタイマー制御クラス '''
    ONE_SHOT = const(0)
    PERIODIC = const(1)

    # 100クロックに一回、IRQを発生させる（実測した）
    @rp2.asm_pio()
    def irq_program():
        irq(rel(0))     # IRQ 0 を発生
        nop() [31]
        nop() [31]
        nop() [31]
        nop() [2]
        wrap()

    def __init__(self, id=0) -> None:
        self._id = id
        self._callback = None
        self._period = 0
        self._counter = 0
        self._mode = MyTimer.PERIODIC

        # 周波数 100,000Hz なので、１クロックは 0.01msec
        self.sm = rp2.StateMachine(self._id, MyTimer.irq_program, freq=100000)
        self.sm.irq(self.__intercepter)


    def __intercepter(self, sm):
        ''' タイマー制御用callback関数 '''
        _now = time.ticks_ms()
        if time.ticks_diff(_now, self._spoint) >= self._period:
            if self._mode == MyTimer.ONE_SHOT:
                self.sm.active(0)   # ステートマシンを無効化
            else:
                self._spoint = _now
            if self._callback:
                self._callback(self)

    def init(self, mode=PERIODIC, period=10, callback=None):
        ''' タイマーを初期化する '''
        assert callable(callback), "callback must be a callable object."
        self._callback = callback

        self._mode = mode
        self._period = period
        self._spoint = time.ticks_ms()

        self.sm.active(1)  # ステートマシンを有効化

    def deinit(self):
        self.sm.active(0)

class Edas():
    ''' 並行処理クラス '''
    class Suspender():
        ''' with構文を使ってturnの開始を一時的にfreezeさせるクラス '''
        def __init__(self, freezetime=5):
            self.freezetime = freezetime

        def __enter__(self):
            Edas.__freeze_handler(self.freezetime)

        def __exit__(self, exc_type, exc_value, traceback):
            Edas.__defreeze_handler()

    # タスクの状態
    NULL = const(0)     # 無効
    START = const(1)    # 開始/再開（EXECに移行）
    PAUSE = const(2)    # 停止
    EXEC = const(3)     # 実行中
    S_PAUSE = const(4)  # 実行中で SYNC停止待ち
    S_END = const(5)    # 実行中で SYNC終了待ち
    END = const(6)      # 終了（終了リストに移行）
    DONE = const(9)     # 終了（終了リストに以降済み）

    _state_list = ["NULL", "START", "PAUSE", "EXEC", "S_PAUSE", "S_END", "END",
                   "unknown", "unknown", "DONE", "unknown"]

    # タスクの性質
    CORE = const(0)         # システム制御用
    PERSISTENT = const(1)   # 継続的なタスク
    BASIC = const(2)        # 通常タスク
    ANCILLARY = const(3)    # いつ終了させても問題ないタスク
    UNKNOWN = const(4)      # 管理対象外
    # タスクの性質のセット
    TASK_NATURE_SET = {CORE, PERSISTENT, BASIC, ANCILLARY}

    _nature_list = ["CORE", "PERSISTENT", "BASIC", "ANCILLARY", "UNKNOWN"]

    # タスクのセッション実行結果
    SYNC = const(22)    # SYNCポイントに達した
    IEND = const(-1)    # タスク（ジェネレータ）が終了した

    TIMER_ID = 0    # タイマーID
    # if TIMER_ID == -1:
    #     __timer = Timer(TIMER_ID)       # タイマーモジュール（仮想）
    # else:
    #     __timer = MyTimer(TIMER_ID)     # タイマーモジュール（StateMachine）


    __edata = []                # タスクのリスト
    __tdata = []                # 終了したタスクのリスト

    __task_count = [0] * (len(TASK_NATURE_SET) + 1)     # 実行中のタスクのカウント（性質別）

    __interval = 100            # イベントループの実行間隔(msec)
    __interval_min = 5          # 実行間隔の最小値
    __is_loop_active = False    # イベントループが実行中か
    __tracelevel = 0            # トレースレベル

    __ticks_ms = time.ticks_ms()    # handlerの現在のturnの開始時刻（同期用）
    __touched_point = __ticks_ms    # タスク実行ポイント（最後に BASICのタスクを実行した時刻）
    __taskidle_time_ms = 0          # タスクが実行されない時間（msef）
    __task_is_idle = False          # turn中、BASICのタスクが実行されなかったら True
    __endpoint = 0              # handlerの終了時刻（デバッグ用）
    __entpoint = 0              # handlerの開始時刻（デバッグ用）

    __freezed = False           # handler凍結中かどうか
    __freezetime = 2            # 一回のfreeze時間(ms)

    def __init__(self, gen, name=None, previous_task=None, pause=False, on_cancel=None,
                 terminate_by_sync=False, task_nature=BASIC, volatile=True):

        assert is_generator(gen), "<gen> must be generator"

        _name = name if name else repr(gen).split(' ')[-1][:-1]
        _type = repr(gen).split(' ')[2][1:-1]

        self._gen = gen             # コルーチンオブジェクト（ジェネレータオブジェクト）
        self._state = Edas.NULL     # タスクの動作状態
        self.name = _name           # タスクの名前
        self.type = _type           # タスクのタイプ（コルーチン名）
        self._terminate_by_sync = terminate_by_sync     # 'SYNC' で終了するかどうか
        
        assert on_cancel is None or callable(on_cancel),\
              "Argument 'on_cancel' must be callable"
        self._on_cancel = on_cancel     # タスク終了後に動く関数
        self._canceled = False          # cancelされたかどうか

        self._follows = []          # 後続のタスクリスト
        self._task_nature = task_nature \
                            if task_nature in Edas.TASK_NATURE_SET \
                            else Edas.UNKNOWN       # タスクの性質
        self._volatile = volatile   # タスク終了後に削除されるかどうか

        self._start_point = 0       # 開始時刻
        self._end_point = 0         # 終了時刻
        self._result = None         # タスクの実行結果

        if not previous_task:   # 先行タスク指定なし（単独タスク）
            # pause=Falseの時は開始、pause=Trueの時は停止（resume待ち）
            self._state = Edas.START if not pause else Edas.PAUSE
            Edas.__traceprint(11, "--> init ", self)

        else:                   # 先行タスク指定あり
            if previous_task in Edas.__edata and previous_task._state != Edas.END:
                # 指定の先行タスクが存在していて、動作状態が ENDではない場合
                self._state = Edas.PAUSE         # 自身は PAUSEとして登録
                Edas.__traceprint(11, "--> init ", self)

                previous_task._follows.append(self)  # 先行タスクの _followsに追加
                Edas.__traceprint(11, "  --> follow to ", previous_task)
            else:
                # 指定の先行タスクが存在しないか、ENDの場合
                self._state = Edas.START         # 即実行（STARTとして登録）
                Edas.__traceprint(11, "--> init ", self)
                Edas.__traceprint(11, "('followto' is not exist!!) ")

        if self._state == Edas.START:
            Edas.__task_is_idle = False

        Edas.__edata.append(self)   # タスクリストに登録

    @classmethod
    def __freeze_handler(cls, freezetime):
        cls.__traceprint(11, "** freeze_handler ")
        cls.__freezetime = min(freezetime, 20)
        cls.__freezed = True

    @classmethod
    def __defreeze_handler(cls):
        cls.__traceprint(11, "** defreeze_handler ")
        cls.__freezed = False

    @classmethod
    def ticks_ms(cls):
        ''' ハンドラーの現在のturn の時刻(ms)を返す '''
        return cls.__ticks_ms

    # ハンドラー ======================================================
    @classmethod
    def _handler(cls, timer):
        ''' 定期的に起動されるハンドラー '''
        cls.__entpoint = time.ticks_ms()

        cls.__traceprint(28, f"  + ---- loopperiod={time.ticks_diff(time.ticks_ms(), cls.__endpoint)}")
        cls.__endpoint = time.ticks_ms()

        # freeze（一時停止）処理
        if cls.__freezed:
            cls.__traceprint(11, f"==== freezed({cls.__freezetime}) ====")
            timer.init(mode=Timer.ONE_SHOT, period=cls.__freezetime, callback=cls._handler)
            return

        # 事前処理 ----------------------------------------------------
        cls.__traceprint(24, "alignment process.....")
        cls.__ticks_ms = time.ticks_ms()

        for edas in list(cls.__edata):

            if edas._state == cls.START:    # 開始/再開タスク
                edas._state = cls.EXEC          # 「実行中」に変更
                edas._start_point = cls.__ticks_ms  # 実行開始ポイント
                cls.__traceprint(14, "      >>> ", edas, previus_state=cls.START)

            elif edas._state == cls.END:    # 終了タスク
                edas._end_point = cls.__ticks_ms    # 実行終了ポイント
                if edas._canceled and edas._on_cancel:
                    print("Execute on_canceled")
                    edas._on_cancel()
                cls._set_follows(edas)          # 後続タスクを「実行中」に変更
                edas._gen.close()               # ジェネレータ・オブジェクトを停止する
                edas._state = cls.DONE
                edas._gen = None                # ジェネレータ・オブジェクトの参照を削除
                edas._follows = []              # 後続タスクのリストを削除
                cls.__edata.remove(edas)        # END -> タスクリストから削除

                if edas._result or not edas._volatile:
                    cls.__tdata.append(edas)    # 終了タスクリストへ登録
                    cls.__traceprint(14, "      >>> ", edas)
                    cls.__traceprint(14, f"      {edas._result=}")
                else:                           # delete
                    cls.__traceprint(14, "      >>> ", edas, aftermessage="  deleted")
                    pass
                    # del edas

        # 実行処理 ----------------------------------------------------
        # 実行中のタスクのカウント（性質別）をクリアしている
        cls.__task_count[:] = [0] * (len(cls.TASK_NATURE_SET) + 1)

        cls.__traceprint(22, "turn.....")
        for edas in list(cls.__edata):
            cls.__traceprint(32, "  *     ", edas)
            if edas._state not in [cls.EXEC, cls.S_PAUSE, cls.S_END]:
                continue
            cls.__task_count[edas._task_nature] += 1
            try:
                _ret = next(edas._gen)      # ジェネレータ・オブジェクトを 1ステップ実行
            except StopIteration as e:      # ジェネレータ・オブジェクトが終了
                edas._result = e.value
                _ret = cls.IEND

            _pstate = edas._state
            if _ret == cls.IEND:        # ジェネレータ・オブジェクトの終了を検出
                edas._state = cls.END       # EXEC、S_PAUSE、S_END -> END
                cls.__traceprint(14, "   >> END ", edas, previus_state=_pstate)

            elif _ret == cls.SYNC:      # SYNCを検出
                if edas._state == cls.S_PAUSE:  # S_PAUSE -> PAUSE
                    edas._state = cls.PAUSE
                    cls.__traceprint(15, "   > SYNC ", edas, previus_state=_pstate)
                elif edas._state == cls.S_END:
                    edas._state = cls.END       # S_END -> END
                    cls.__traceprint(15, "   > SYNC ", edas, previus_state=_pstate)
                else:                           # S_PAUSE、S_END 以外は何もしない
                    cls.__traceprint(18, "   > SYNC ", edas)

        # タスクアイドルタイム（nature=BASIC のタスクが動いていない時間）を計算
        if cls.__task_count[cls.BASIC]:     # タスクが実行されている
            cls.__touched_point = cls.__ticks_ms    # タスク実行ポイントをセット
            cls.__taskidle_time_ms = 0
            cls.__task_is_idle = False
        else:                               # タスクアイドル
            cls.__taskidle_time_ms = time.ticks_diff(cls.__ticks_ms, cls.__touched_point)
            cls.__task_is_idle = True

        _timespent = time.ticks_diff(time.ticks_ms(), cls.__entpoint)
        cls.__traceprint(22, f"  +   -- {cls.__task_count=}, {cls.__taskidle_time_ms=}")
        cls.__traceprint(28, f"  +   -- timespent={_timespent}")
        _period = max(cls.__interval - _timespent, cls.__interval_min)

        if cls.__is_loop_active:
            timer.init(mode=Timer.ONE_SHOT, period=_period, callback=cls._handler)
        return

    @classmethod
    def _set_follows(cls, edas):
        ''' 後続タスク処理 '''
        for fedas in edas._follows:    # 指定タスクの全ての「後続タスク」について
            if fedas in cls.__edata:
                if fedas._state == cls.PAUSE:   # 「停止中」だったら
                    fedas._state = cls.EXEC         # 「実行」に変更
                    fedas._start_point = cls.__ticks_ms  # 実行開始ポイント
                    cls.__traceprint(14, "--> shift to EXEC", fedas, previus_state=cls.PAUSE)
                else:                           # 「停止中」以外
                    cls.__traceprint(8, "--> can't shift to EXEC**", fedas)
            else:                               # タスクリストに存在しない
                cls.__traceprint(8, "--> can't find**", fedas)

    @classmethod
    def loop_start(cls, loop_interval=None, tracelevel=0, id=0):
        ''' イベントループを開始する '''
        if tracelevel is not None:
            cls.__tracelevel = tracelevel
        if loop_interval is not None:
            cls.__interval = max(loop_interval, cls.__interval_min)
        if not cls.__is_loop_active:
            cls.__is_loop_active = True
            cls.__touched_point = cls.__ticks_ms    # タスク実行ポイントをセット

            cls.TIMER_ID = id
            cls.__traceprint(11, f"Edas.loop_start {cls.TIMER_ID=}")
            if cls.TIMER_ID == -1:
                cls.__timer = Timer(cls.TIMER_ID)       # タイマーモジュール（仮想）
            else:
                cls.__timer = MyTimer(cls.TIMER_ID)     # タイマーモジュール（StateMachine）

            cls.__timer.init(mode=Timer.ONE_SHOT, period=cls.__interval, callback=cls._handler)

    @classmethod
    def loop_stop(cls):
        ''' イベントループを停止する '''
        cls.__is_loop_active = False

    @classmethod
    def cancel_tasks(cls, natures=[BASIC, ANCILLARY], sync=False):
        ''' 動作中の指定の性質のタスクを終了する '''
        for edas in list(cls.__edata):
            if edas._task_nature in natures:
                edas.cancel(sync=sync)

    @classmethod
    def cancel_basic_tasks(cls, sync=False):
        ''' 動作中の全ての通常タスク（task_nature=BASIC）を終了する '''
        for edas in list(cls.__edata):
            if edas._task_nature == Edas.BASIC:
                edas.cancel(sync=sync)

    @classmethod
    def wait_for_idle(cls, timeout=None):
        ''' 動作中の全ての通常タスク（task_nature=BASIC）の終了を待つ '''
        if timeout:
            _wtimeout = int(timeout * 1000)
            _spoint = time.ticks_ms()
        while(not timeout or time.ticks_diff(time.ticks_ms(), _spoint) < _wtimeout):
            if cls.__task_is_idle:
                break

    @classmethod
    def show_edas(cls):
        ''' タスクリスト中のタスクの一覧を表示する（デバッグ用） '''
        for _no, edas in enumerate(list(cls.__edata)):
            cls.__traceprint(0, f"{_no}: ", edas)

    @classmethod
    def show_done(cls):
        ''' 終了したタスクの一覧を表示する（デバッグ用） '''
        for _no, edas in enumerate(list(cls.__tdata)):
            cls.__traceprint(0, f"{_no}: ", edas)

    @classmethod
    def stop_edas(cls, name=None, sync=False):
        ''' タスクを停止する（デバッグ用） '''
        for edas in list(cls.__edata):
            if name is None:
                edas.stop(sync)
            elif edas.name == name:
                print("Hit!!")
                edas.stop(sync)
                return
        print(f"can't find edas <{name}>")

    @classmethod
    def _str_state(cls, state):
        ''' 指定タスクの状態を文字列で返す（デバッグ用） '''
        return cls._state_list[min(state, len(cls._state_list))]

    @classmethod
    def _str_nature(cls, nature):
        ''' 指定タスクの性質を文字列で返す（デバッグ用） '''
        return cls._nature_list[nature]

    @classmethod
    def _get_taskcount(cls, nature = None):
        ''' 直前の turnで、それぞれの性質のタスクが動いた本数を返す '''
        if nature in cls.TASK_NATURE_SET:
            return cls.__task_count[nature]
        elif nature == cls.UNKNOWN:
            return cls.__task_count[cls.UNKNOWN]
        else:
            return sum(cls.__task_count)

    @classmethod
    def idle_time(cls):
        ''' 通常のタスク（task_nature=BASIC）が動作していない時間を返す '''
        return cls.__taskidle_time_ms / 1000

    @classmethod
    def __traceprint(cls, level, message, myself=None, previus_state=None, aftermessage=""):
        ''' デバッグ用プリント
            level 21～32 :もっと細かいトレース
            level 11～20 :状態変化出力
            level  ～ 10  :エラー出力
        '''
        if cls.__tracelevel >= level:
            if myself:
                _strstate = f" [{cls._str_state(myself._state)}]"
                _strnature = f" <{cls._str_nature(myself._task_nature)}>"
                if previus_state:
                    _strstate = f" [{cls._str_state(previus_state)}]->" + _strstate

                print(f"{message}"   + f" name={myself.name} ({myself.type})" +
                      _strnature +  _strstate + aftermessage)

                for yourself in myself._follows:
                    print("        + " +
                          f" name={yourself.name} ({yourself.type})" +
                          f" [{cls._str_state(yourself._state)}]" +
                          "")
            else:
                print(f"{message}")

    def resume(self):
        ''' タスクを開始/再開する '''
        if self in Edas.__edata:
            _pstate = self._state
            if self._state in [Edas.PAUSE, Edas.S_PAUSE]:
                self._state = Edas.START
                Edas.__traceprint(11, "--> resume ", self, previus_state=_pstate)
            else:
                Edas.__traceprint(8, "--> can't resume** ", self)
        else:
            Edas.__traceprint(8, "--> can't find** ", self)

    def pause(self, sync=True):
        ''' タスクを中断する '''
        _sync = sync and self._terminate_by_sync
        if self in Edas.__edata:
            _pstate = self._state
            if self._state in [Edas.EXEC, Edas.S_PAUSE]:
                self._state = Edas.S_PAUSE if _sync else Edas.PAUSE
                Edas.__traceprint(11, "--> pause ", self, previus_state=_pstate)
            else:
                Edas.__traceprint(8, "--> can't pause** ", self)
        else:
            Edas.__traceprint(8, "--> can't find** ", self)

    def cancel(self, prevent_next_task=False, sync=True):
        ''' タスクを終了する '''
        _sync = sync and self._terminate_by_sync
        if self in Edas.__edata:
            _pstate = self._state
            if self._state in [Edas.EXEC, Edas.S_PAUSE, Edas.S_END]:
                self._state = Edas.S_END if _sync else Edas.END
                if prevent_next_task:
                    self._follows = []
                self._canceled = True
                Edas.__traceprint(11, "--> cancel  ", self, previus_state=_pstate)
            elif self._state in [Edas.START, Edas.PAUSE]:
                self._state = Edas.END
                self._canceled = True
                Edas.__traceprint(11, "--> cancel  ", self, previus_state=_pstate)
            else:
                Edas.__traceprint(8, "--> can't cancel**  ", self)
        else:
            Edas.__traceprint(8, "--> can't find** ", self)

    def done(self):
        ''' タスクの終了を判定する '''
        return self not in Edas.__edata
        return (self._state == Edas.DONE)

    def result(self):
        ''' タスクの終了結果を返す '''
        if self in Edas.__tdata:
            ret = self._result
            if self._volatile:
                Edas.__tdata.remove(self)
            return ret
        else:
            return None

    @classmethod
    def after(cls, delay, function):
        cls.__traceprint(9, f"===== after called {delay=}, {function=}")
        return Edas.after_ms(delay * 1000, function)

    @staticmethod
    def after_ms(delay, function):
        def _after(delay, function):
            _ctime = CheckTime()
            while _ctime.wait(delay):
                yield
            function()
        return Edas(_after(delay, function))

    @staticmethod
    def y_oneshot(func):
        ''' funcを一回だけ実行してすぐ終了するタスクジェネレータ '''
        func()
        return
        yield "dummy for oneshot generator"

    @staticmethod
    def y_sleep(second):
        ''' second秒が経過するまで yieldを繰り返すタスクジェネレータ<br>
            yield from Edas.y_sleep(second) で呼び出すこと。
        '''
        _wait_ms = int(second * 1000)
        _now = Edas.ticks_ms()
        while time.ticks_diff(Edas.ticks_ms(), _now) < _wait_ms:
            yield

    @staticmethod
    def y_sleep_ms(ms):
        ''' ms ミリ秒が経過するまで yieldを繰り返すタスクジェネレータ<br>
            yield from Edas.y_sleep_ms(ms) で呼び出すこと。
        '''
        _now = Edas.ticks_ms()
        while time.ticks_diff(Edas.ticks_ms(), _now) < ms:
            yield


class CheckTime():
    ''' 経過時間(msec)をチェックするクラス '''
    def __init__(self) -> None:
        self._ms = Edas.ticks_ms()      # 意識している時刻

    def set(self, ms=None):
        ''' 基準時刻を trun時刻、または指定時刻に変更する '''
        self._ms = int(ms) if ms else Edas.ticks_ms()
        return self._ms

    def add_ms(self, delta):
        ''' 意識している時刻を delta(ms) だけ加算する '''
        self._ms = time.ticks_add(self._ms, int(delta))
        return self._ms

    def ref_time(self):
        ''' 意識している時刻を返す '''
        return self._ms

    def y_wait_ms(self, wait_ms, update=False):
        ''' wait_ms 時間が経過するまで yieldを繰り返すタスクジェネレータ<br>
            yield from _checktime.y_wait_ms(wait_ms) で呼び出すこと。
        '''
        while time.ticks_diff(Edas.ticks_ms(), self._ms) < int(wait_ms):
            yield
        if update:
            self._ms = time.ticks_add(self._ms, int(wait_ms))
            
    # def wait(self, wait_ms) -> bool:
    #     ''' wait_ms 時間が経過するまでTrue、経過したらFalseになる。
    #     '''
    #     if time.ticks_diff(Edas.ticks_ms(), self._ms) < int(wait_ms):
    #         return True
    #     return False

if __name__ == '__main__':
    from machine import Pin

    def y_blink(led, ontime, offtime, n):
        _ctime = CheckTime()
        _count = 0
        try:
            while not n or _count < n:
                led.on()
                yield from _ctime.y_wait_ms(ontime, update=True)
                led.off()
                yield from _ctime.y_wait_ms(offtime, update=True)
                yield Edas.SYNC
                _count += 1
            return "**OWARIDAYO**"  # 最後まで実行されれば値を返す
        # except GeneratorExit as e:  # 途中で close()された場合
        #     pass
        finally:                    # ジェネレータが終了した
            led.off()


    print(__doc__)
    print(f"version = {__version__}")
    Edas.loop_start(tracelevel=14, loop_interval=100, id=0)
    time.sleep(1)

    led1 = Pin(16, Pin.OUT)
    led2 = Pin(17, Pin.OUT)
    task1 = Edas(y_blink(led1, 1000, 200, 1), name="task1", terminate_by_sync=False, volatile=False)
    task2 = Edas(y_blink(led2, 800, 500, 5), previous_task=task1, terminate_by_sync=True)
    # Eloop.start()

    for i in range(1000):
        # with Eloop.Suspender():
        print(f"---- round {i} ----")
        # if i == 1:
        #     task1.cancel()
        # print(f"{Edas._get_taskcount()=}")
        # print(f"{Edas._get_taskcount(Edas.BASIC)=}")
        print(f"{Edas.idle_time()=}")

        if Edas.idle_time() > 5.0:
            break
        time.sleep_ms(3000)

    Edas.show_done()
    print(f"{task1.done()=}")
    print(f"{task1.result()=}")
    Edas.show_done()
    print(f"{task2.done()=}")
    print(f"{task2.result()=}")
    Edas.show_done()
    print(f"{task1.result()=}")
    print(f"{task2.result()=}")

    print()
    print(f"name ={task1.name}")
    print(f"start={task1._start_point}")
    print(f"end  ={task1._end_point}")
    print(f"lifetime={time.ticks_diff(task1._end_point, task1._start_point):,}")
