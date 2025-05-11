__doc__ = \
'''-- Edas module for MycroPython'''
''' CheckTimeの y_wait に update指定を追加 '''
__version__ = "0.09.04"
import time
from micropython import const
from machine import Timer

TypeGenerator = type((lambda: (yield))())


def is_generator(obj):
    ''' ジェネレータオブジェクトの判定 '''
    return isinstance(obj, TypeGenerator)


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
    VOLATILE = const(3)     # いつ終了させても問題ないタスク
    FLASH = const(4)
    UNKNOWN = const(5)      # 管理対象外
    # タスクの性質のセット
    TASK_NATURE_SET = {CORE, PERSISTENT, BASIC, VOLATILE, FLASH}

    _nature_list = ["CORE", "PERSISTENT", "BASIC", "VOLATILE", "FLASH", "UNKNOWN"]

    # タスクのセッション実行結果
    SYNC = const(22)    # SYNCポイントに達した
    IEND = const(-1)    # タスク（ジェネレータ）が終了した

    TIMER_ID = -1 # ハードウェアタイマーID


    __edata = []                # タスクのリスト
    __tdata = []                # 終了したタスクのリスト

    __task_count = [0] * (len(TASK_NATURE_SET) + 1)     # 実行中のタスクのカウント（性質別）

    __interval = 100            # イベントループの実行間隔(msec)
    __interval_min = 5          # 実行間隔の最小値
    __is_loop_active = False    # イベントループが実行中か
    __tracelevel = 0            # トレースレベル
    __timer = Timer(TIMER_ID)   # タイマーモジュール

    __ticks_ms = time.ticks_ms()    # handlerの現在のturnの開始時刻（同期用）
    __touched_point = __ticks_ms    # タスク実行ポイント（最後に BASICのタスクを実行した時刻）
    __taskidle_time_ms = 0          # タスクが実行されない時間（msef）
    __task_is_idle = False          # turn中、BASICのタスクが実行されなかったら True
    __endpoint = 0              # handlerの終了時刻（デバッグ用）
    __entpoint = 0              # handlerの開始時刻（デバッグ用）

    __freezed = False           # handler凍結中かどうか
    __freezetime = 2            # 一回のfreeze時間(ms)

    # __heartbeat = Bootsel_button()
    # __heartbeatON = None
    # __heartbeatOFF = None

    def __init__(self, gen, name=None, previous_task=None, pause=False,
                 terminate_by_sync=False, task_nature=BASIC):

        assert is_generator(gen), "<gen> must be generator"

        _name = name if name else repr(gen).split(' ')[-1][:-1]
        _type = repr(gen).split(' ')[2][1:-1]

        self._gen = gen             # コルーチンオブジェクト（ジェネレータオブジェクト）
        self._state = Edas.NULL     # タスクの動作状態
        self.name = _name           # タスクの名前
        self.type = _type           # タスクのタイプ（コルーチン名）
        self._terminate_by_sync = terminate_by_sync     # 'SYNC' で終了するかどうか
        self._follows = []          # 後続のタスクリスト
        self._task_nature = task_nature \
                            if task_nature in Edas.TASK_NATURE_SET \
                            else Edas.UNKNOWN       # タスクの性質

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

        # 事前処理
        cls.__traceprint(24, "alignment process.....")
        cls.__ticks_ms = time.ticks_ms()

        for edas in list(cls.__edata):

            if edas._state == cls.START:    # 開始/再開タスク
                edas._state = cls.EXEC          # 「実行中」に変更
                cls.__traceprint(14, "      >>> ", edas, previus_state=cls.START)

            elif edas._state == cls.END:    # 終了タスク
                cls._set_follows(edas)          # 後続タスクを「実行中」に変更
                cls.__edata.remove(edas)        # END -> タスクリストから削除
                edas._state = cls.DONE          
                cls.__traceprint(14, "      >>> ", edas, aftermessage="  deleted")
                cls.__tdata.append(edas)
                if edas._result:
                    cls.__traceprint(14, f"     {edas._result=}")

        # 実行処理
        # if cls.__heartbeatON:
        #     cls.__heartbeatON.on()

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
            except StopIteration as e:       # ジェネレータ・オブジェクトが終了
                edas._result = e
                _ret = cls.IEND

            _pstate = edas._state
            if _ret == cls.IEND:        # ジェネレータ・オブジェクトの終了を検出
                edas._state = cls.END        # EXEC、S_PAUSE、S_END -> END
                cls.__traceprint(14, "   >> END ", edas, previus_state=_pstate)

            elif _ret == cls.SYNC:      # SYNCを検出
                if edas._state == cls.S_PAUSE:   # S_PAUSE -> PAUSE
                    edas._state = cls.PAUSE
                    cls.__traceprint(15, "   > SYNC ", edas, previus_state=_pstate)
                elif edas._state == cls.S_END:
                    edas._state = cls.END        # S_END -> END
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
        cls.__traceprint(22, f"  +   -- taskcount={cls.__task_count}")
        cls.__traceprint(28, f"  +   -- timespent={_timespent}")
        _period = max(cls.__interval - _timespent, cls.__interval_min)
        # if cls.__heartbeatON:
        #     cls.__heartbeatON.off()
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
                    cls.__traceprint(14, "--> shift to EXEC", fedas, previus_state=cls.PAUSE)
                else:                           # 「停止中」以外
                    cls.__traceprint(8, "--> can't shift to EXEC**", fedas)
            else:                               # タスクリストに存在しない
                cls.__traceprint(8, "--> can't find**", fedas)

    @classmethod
    def loop_start(cls, loop_interval=None, tracelevel=0):
        ''' イベントループを開始する '''
        # cls.__heartbeatON = LED("LED")

        if tracelevel is not None:
            cls.__tracelevel = tracelevel
        if loop_interval is not None:
            cls.__interval = max(loop_interval, cls.__interval_min)
        if not cls.__is_loop_active:
            cls.__is_loop_active = True
            cls.__touched_point = cls.__ticks_ms    # タスク実行ポイントをセット
            cls.__timer.init(mode=Timer.ONE_SHOT, period=cls.__interval, callback=cls._handler)

    @classmethod
    def loop_stop(cls):
        ''' イベントループを停止する '''
        cls.__is_loop_active = False

    @classmethod
    def cancel_basic_tasks(cls, sync=True):
        ''' 動作中の全ての通常タスク（task_nature=BASIC）を終了する '''
        for edas in list(cls.__edata):
            # print(f"name={edas.name}, stat={edas._state}, nature={edas._task_nature}")
            if edas._task_nature == Edas.BASIC:
                edas.cancel(sync=sync)

    @classmethod
    def wait_for_idle(cls, timeout=1.0):
        ''' 動作中の全ての通常タスク（task_nature=BASIC）の終了を待つ '''
        _wtimeout = int(timeout * 1000)
        _spoint = time.ticks_ms()
        while(time.ticks_diff(time.ticks_ms(), _spoint) < _wtimeout):
            if cls.__task_is_idle:
                # print("end")
                break
        # else:
        #     print("timeout")

    @classmethod
    def show_edas(cls):
        ''' タスクリスト中のタスクの一覧を表示する（デバッグ用） '''
        for _no, edas in enumerate(list(cls.__edata)):
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
            if self._state == Edas.PAUSE:
                self._state = Edas.START
                Edas.__traceprint(11, "--> resume ", self, previus_state=Edas.PAUSE)
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

    def cancel(self, sync=True):
        ''' タスクを終了する '''
        print(f"{sync=}, {self._terminate_by_sync=}")
        _sync = sync and self._terminate_by_sync
        if self in Edas.__edata:
            _pstate = self._state
            if self._state in [Edas.EXEC, Edas.S_PAUSE, Edas.S_END]:
                print(f"{_sync=}")
                self._state = Edas.S_END if _sync else Edas.END
                Edas.__traceprint(11, "--> cancel  ", self, previus_state=_pstate)
            elif self._state in [Edas.START, Edas.PAUSE]:
                self._state = Edas.END
                Edas.__traceprint(11, "--> cancel  ", self, previus_state=_pstate)
            else:
                Edas.__traceprint(8, "--> can't cancel**  ", self)
        else:
            Edas.__traceprint(8, "--> can't find** ", self)

    def done(self):
        ''' タスクの終了を判定する '''
        return (self._state == Edas.DONE)

    def result(self):
        return self._result

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

    # @staticmethod
    # def y_wait_while(wait_ms):
    #     ''' wait_ms 時間が経過するまで yieldを繰り返す。<br>
    #         yield from Edas.wait_while(wait_ms) で呼び出すこと。
    #     '''
    #     _now = Edas.ticks_ms()
    #     while time.ticks_diff(Edas.ticks_ms(), _now) < wait_ms:
    #         yield


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

    def y_wait(self, wait_ms, update=False):
        ''' wait_ms 時間が経過するまで yieldを繰り返す。<br>
            yield from _checktime.y_wait(wait_ms) で呼び出すこと。
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


