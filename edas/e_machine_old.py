__doc__ = \
'''-- Edas module for MycroPython'''
''' CheckTimeの y_wait_ms に update指定を追加 '''
__version__ = "0.09.04"
import time
from micropython import const
from machine import Timer, Pin, Signal, PWM
import rp2
from e_module import Edas, CheckTime

class Eloop():
    class Suspender():
        ''' with構文を使ってturnの開始を一時的に停止させるクラス '''
        def __init__(self, duration: int=5):
            ''' turnの開始を一時的に停止する

                args:
                    duration: int（停止する単位時間 msec）
            '''
            self.freezetime = duration

        def __enter__(self):
            Edas.__freeze_handler(self.freezetime)

        def __exit__(self, exc_type, exc_value, traceback):
            Edas.__defreeze_handler()

    def __init__(self) -> None:
        pass

    @staticmethod
    def start(loop_interval: int|None=None, tracelevel: int=0, id=0):
        ''' Edasのイベントループを開始する

            args:
                loop_interval: int（イベントループの間隔 msec）
                tracelevel: int（トレース情報出力レベル）
                id: int（タイマーID -1、0 ～ 7）
        '''
        Edas.loop_start(loop_interval, tracelevel, id=id)

    @staticmethod
    def stop():
        ''' Edasのイベントループを停止する '''
        Edas.loop_stop()

    @staticmethod
    def create_task(gen, name=None, previous_task=None, pause=False, on_cancel=None,
                    terminate_by_sync=False, task_nature=Edas.BASIC, volatile=True):
        ''' 新しいタスクを生成し、イベントループに登録する

            args:
                gen: generator（タスクとして動作するジェネレータオブジェクト）
                name: str（タスクにつける名前）
                previous_task: <edas>（先行タスク）
                pause: bool（登録後すぐ実行するかどうか）
                on_cancel: callable（タスクがキャンセルされた時に実行する処理）
                terminate_by_sync: bool（'SYNC' で終了するかどうか）
                task_nature: int（タスクの性質）
                volatile: bool（タスク終了時に消去されるかどうか）
            return:
                <edas> Edasタスクオブジェクト
        '''


        return Edas(gen, name=name, previous_task=previous_task, pause=pause, on_cancel=on_cancel,
                    terminate_by_sync=terminate_by_sync, task_nature=task_nature, volatile=volatile)

    @staticmethod
    def idle_time():
        ''' 通常のタスク（task_nature=BASIC）が動作していない時間を返す '''
        return Edas.idle_time()

    @staticmethod
    def cancel_tasks(natures=[Edas.BASIC, Edas.ANCILLARY], sync=False):
        ''' 動作中の指定の性質のタスクを終了する '''
        Edas.cancel_tasks(natures=natures, sync=sync)

    @staticmethod
    def cancel_basic_tasks(sync=False):
        ''' 動作中の全ての通常タスク（task_nature=BASIC）を終了する '''
        Edas.cancel_basic_tasks(sync=sync)

    @staticmethod
    def wait_for_idle(timeout=None):
        ''' 動作中の全ての通常タスク（task_nature=BASIC）の終了を待つ '''
        Edas.wait_for_idle(timeout=timeout)

    @staticmethod
    def y_sleep(second):
        ''' second秒が経過するまで yieldを繰り返すタスクジェネレータ<br>
            yield from Edas.y_sleep(second) で呼び出すこと。
        '''
        _wait_ms = int(second * 1000)
        _now = Edas.ticks_ms()
        while time.ticks_diff(Edas.ticks_ms(), _now) < _wait_ms:
            yield

# -------------------------- Button class  below ---------------------------------------------
class KeyList():
    ''' (key, value) のリストを制御する Dicもどきクラス
        MycroPythonの Dicでは Pinオブジェクトをkeyにできなかったための代案
    '''
    def __init__(self):
        self._klist: list[list[object]] = []

    def __setitem__(self, key, value):
        for _item in self._klist:
            if _item[0] == key:
                _item[1] = value
                return
        self._klist.append([key, value])
        return

    def __getitem__(self, key):
        for _item in self._klist:
            if _item[0] == key:
                return _item[1]
        return None

    def __delitem__(self, key):
        for i, _item in enumerate(self._klist):
            if _item[0] == key:
                del self._klist[i]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self._klist):
            result = self._klist[self.index]
            self.index += 1
            return result
        raise StopIteration

    def __len__(self):
        return len(self._klist)

    def keys(self):
        return [item[0] for item in self._klist]

    def values(self):
        return [item[1] for item in self._klist]

    def items(self):
        return [(item[0], item[1]) for item in self._klist]


class Bootsel_button():
    ''' bootsel_button を他のPin入力と同様に扱うためのクラス '''
    def value(self):
        return rp2.bootsel_button()


class Button():
    ''' 押しボタンの状態を取得するクラス '''
    PRESSED = const(1)      # ボタンが押された
    RELEASED = const(2)     # ボタンが離された
    HELD = const(3)         # ボタンが長押しされた
    REPEATED = const(4)     # ボタンが押し続けられた

    __plist = KeyList()     # Pinを登録するリスト（Dicもどき）

    __loop_period = 100     # Timerの周期
    __loop_point = 0        # ボタンloopの起点
    # __loop_point = time.ticks_ms()   # ボタンloopの起点

    __touched_point = 0     # ボタンが最後に触れられた時間
    __idle_time_ms = 0      # ボタンが触られなかった時間

    __tracelevel = 0
    __default_invert = True

    def __init__(self,
                 pin: Pin | int | Bootsel_button,   # Buttonに割付ける Pin
                 name="noname",     # ボタンの名前（任意）
                 pull_up=None,      # 押してLowなら pull_up=True
                 hold_time=None,    # HELD、REPEATED開始までのディレイ（秒）
                 repeat_time=None,  # REPEATEDのインターバル（秒）
                 on_action=None,    # アクション時に呼び出すファンクション
                 on_pressed=None,
                 on_released=None,
                 on_held=None,
                 ):

        self._invert = pull_up if pull_up is not None else Button.__default_invert

        if isinstance(pin, Bootsel_button):
            self._pin = pin
            self._invert = False
        elif isinstance(pin, int):
            self._pin = Pin(pin, Pin.IN, Pin.PULL_UP if self._invert else Pin.PULL_DOWN)
        else:
            self._pin = pin                 # 割付けられたPin

        self.name = name               # Pinの名前

        # ボタンに変化があったときのfunction
        self._on_action = None
        self._on_pressed = None
        self._on_released = None
        self._on_held = None
        self._on_action_args = ()
        self._on_action_kwargs = {}
        self._on_pressed_args = ()
        self._on_pressed_kwargs = {}
        self._on_released_args = ()
        self._on_released_kwargs = {}
        self._on_held_args = ()
        self._on_held_kwargs = {}

        if on_action:
            self.on_action(on_action)
        if on_pressed:
            self.on_pressed(on_pressed)
        if on_released:
            self.on_released(on_released)
        if on_held:
            self.on_held(on_held)
        
        # repeat_timeがあれば REPEATED
        # repeat_timeがなくて hold_timeがあれば HELD
        self._long_press_mode = Button.REPEATED if repeat_time else Button.HELD if hold_time else 0

        if self._long_press_mode == Button.HELD:
            self._hold_ms = round(hold_time * 1000)         # LONG_PRESS、REPEAT開始までのディレイ（msec）
            # self._hold_ms = float(hold_time) * 1000         # LONG_PRESS、REPEAT開始までのディレイ（msec）
        elif self._long_press_mode == Button.REPEATED:
            self._repeat_ms = round(repeat_time * 1000)     # REPEATのインターバル(msec)
            # self._repeat_ms = float(repeat_time) * 1000     # REPEATのインターバル(msec)
            if hold_time:
                self._hold_ms = round(hold_time * 1000)     # LONG_PRESS、REPEAT開始までのディレイ（msec）
                # self._hold_ms = float(hold_time) * 1000     # LONG_PRESS、REPEAT開始までのディレイ（msec）
            else:
                self._hold_ms = self._repeat_ms

        # handler用
        self._wasON = False             # 前回の状態
        self._dpoint = 0                # 長押し/repeat開始時間の格納用
        self._isHeld = False            # 長押しされた
        self._inrepeat = False          # repeat中

        # 測定用内部情報
        self._pressed_point = time.ticks_ms()       # ボタンが押された時刻
        self._released_point = time.ticks_ms()      # ボタンが離された時刻

        # ボタン情報取得用
        self.interval_time = 0.0    # 前回押された時から今回押されるまでの時間（秒）
        self.inactive_time = 0.0    # 前回解放から押されるまでの時間（秒）
        self.active_time = 0.0      # 押されてから離されるまでの時間（秒）
        self.is_pressed = False     # ボタンが押されている状態か
        self.count = 0              # ボタンが押された回数（REPEATEDはカウントしない）
        self.repeat_count = 0       # repeat回数
        self.reason = 0             # ボタンが押された理由


        Button.__plist[self._pin] = self

    def __del__(self):
        del Button.__plist[self]

    @staticmethod
    def _pop_myself(func):
        ''' Mu() Instant Closureのキーワード引数から myself= を抜き出す '''
        mu_myself = None
        if isinstance(func, Mu):
            if 'myself' in func.kwargs:
                mu_myself = func.kwargs.pop('myself')
        return func, mu_myself

    @classmethod
    def start(cls, pull_up=None, name="Bloop", tracelevel=0, period=0):
        ''' ボタン情報を取得する疑似スレッドを開始する '''
        if pull_up:
            cls.__default_invert = pull_up
        if period:
            cls.__loop_period = min(1000, max(10, period))

        cls.__loop_point = time.ticks_ms()      # ボタンloopの起点
        cls.__touched_point = Edas.ticks_ms()

        cls.__tracelevel = tracelevel
        cls._trace(5, f"* {Button.__loop_period=}")

        return Edas(cls._bloop(), name=name, task_nature=Edas.PERSISTENT)

    @classmethod
    def idle_time(cls):
        return cls.__idle_time_ms / 1000

    @classmethod
    def str_reason(cls, reason):
        ''' 状態コード(reason)に対応する、状態を表す文字列を返す '''
        return ["NONE", "PRESSED", "RELEASED", "HELD", "REPEATED", "unknown"][min(max(reason, 0), 5)]

    @classmethod
    def _trace(cls, level, comment):
        ''' デバッグ用プリント
            level 1～ :エラー、ボタン設定時
            level 10～ :ボタン操作時
            level 20～ :ループ情報
        '''            
        if cls.__tracelevel >= level:
            print(f"{comment}")

    # ボタン情報を取得するループ
    @classmethod
    def _bloop(cls):
        ''' ボタン情報を取得するループ（タスクジェネレータ） '''
        while True:
            # 親ハンドラーから高い周期で呼び出された時に受け流す
            if time.ticks_diff(time.ticks_ms(), cls.__loop_point) < \
                            int(cls.__loop_period - Edas.__interval / 2):
                yield
                continue

            cls._trace(22, f"* period={time.ticks_diff(time.ticks_ms(), cls.__loop_point)}")
            cls.__loop_point = time.ticks_ms()

            for myself in Button.__plist.values():
                _reason = 0
                _isON = myself._pin.value() != myself._invert     # 今回の状態
                if not myself._wasON:       # 前回が OFF
                    if _isON:                   # 今回は ON  -> ボタンが押された！
                        cls.__touched_point = Edas.ticks_ms()        # 触られた！！
                        _reason = cls.PRESSED       # 押された！
                        myself.is_pressed = True
                        myself.count += 1

                        _tpoint = myself._pressed_point             # 前回押された時刻
                        myself._pressed_point = time.ticks_ms()     # 今回押された時刻
                        myself.interval_time = time.ticks_diff(myself._pressed_point,
                                                               _tpoint) / 1000
                        myself.inactive_time = time.ticks_diff(myself._pressed_point,
                                                               myself._released_point) / 1000

                        # 長押しや repeat判定のための前処理        
                        myself.repeat_count = 0
                        myself._isHeld = False
                        if myself._long_press_mode:
                            myself._dpoint = time.ticks_ms()        # 長押し起点時刻
                            myself._inrepeat = False
                            myself._t_repeat_ms = myself._hold_ms

                else:  # 前回が ON
                    cls.__touched_point = Edas.ticks_ms()            # 触られた！！
                    if _isON:               # 今回も ON  -> 押し続けられた！
                        if myself._long_press_mode == cls.HELD and not myself._isHeld:  # 長押し判定
                            if time.ticks_diff(time.ticks_ms(), myself._dpoint)\
                                                                    > myself._hold_ms:
                                _reason = cls.HELD
                                myself._isHeld = True           # 長押しされた！
                                myself._dpoint = time.ticks_ms()

                        elif myself._long_press_mode == cls.REPEATED:                   # repeat 判定
                            if time.ticks_diff(time.ticks_ms(), myself._dpoint)\
                                                                    > myself._t_repeat_ms:
                                _reason = cls.REPEATED          # repeatしている！
                                myself.repeat_count += 1

                                if not myself._inrepeat:  # 初回だったら次回用設定
                                    # 初回の _t_repeat_ms はdelay_ms、次回以降は _interbal_ms
                                    myself._inrepeat = True
                                    myself._t_repeat_ms = myself._repeat_ms

                                myself._dpoint = time.ticks_ms()


                    else:                   # 今回は OFF  -> ボタンが離された！
                        if not myself._isHeld:      # 長押しされていない
                            _reason = cls.RELEASED      # ボタンが離された！
                        myself._isHeld = False
                        myself._released_point = time.ticks_ms()
                        myself.is_pressed = False

                if _reason:   # 設定された functionを実行
                    cls._trace(11, f"** function called  <{myself.name}> " +
                                    f"reason={cls.str_reason(_reason)}")
                    myself.active_time = time.ticks_diff(time.ticks_ms(),
                                                       myself._pressed_point) / 1000
                    myself.reason = _reason
                    myself._do_function()

                myself._wasON = _isON   # 今回の状態を前回の状態として保持
            cls.__idle_time_ms = time.ticks_diff(Edas.ticks_ms(), cls.__touched_point)
            yield

    def _do_function(self):
        ''' ボタンの状態毎に指定されたファンクションを実行する '''
        if self._on_action:
            if Button.__tracelevel:
                _tmsg = f"**** on_action  <{self.name}> reason={Button.str_reason(self.reason)}"
                if self.reason == Button.PRESSED:
                    _tmsg += f" count={self.count}"
                elif self.reason == Button.REPEATED:
                    _tmsg += f" repeat_count={self.repeat_count}"
                Button._trace(10, _tmsg)
                Button._trace(11, f"++++ {self._on_action=}")
            self._on_action(*self._on_action_args, **self._on_action_kwargs)

        if self.reason in [Button.PRESSED, Button.REPEATED]:
            if self._on_pressed:
                if Button.__tracelevel:
                    _tmsg = f"**** on_pressed  <{self.name}> reason={Button.str_reason(self.reason)}"
                    if self.reason == Button.PRESSED:
                        _tmsg += f" count={self.count}"
                    else:
                        _tmsg += f" repeat_count={self.repeat_count}"
                    Button._trace(10, _tmsg)
                    Button._trace(11, f"++++ {self._on_pressed=}")
                self._on_pressed(*self._on_pressed_args, **self._on_pressed_kwargs)

        elif self.reason == Button.HELD:
            if self._on_held:
                if Button.__tracelevel:
                    Button._trace(10, f"**** on_held  <{self.name}> " +
                                    f"reason={Button.str_reason(self.reason)}")
                    Button._trace(11, f"++++ {self._on_held=}")
                self._on_held(*self._on_held_args, **self._on_held_kwargs)

        elif self.reason == Button.RELEASED:
            if self._on_released:
                if Button.__tracelevel:
                    Button._trace(10, f"**** on_released  <{self.name}> " +
                                    f"reason={Button.str_reason(self.reason)}")
                    Button._trace(11, f"++++ {self._on_released=}")
                self._on_released(*self._on_released_args, **self._on_released_kwargs)

    def on_action(self, func, *args, myself=True, **kwargs):
        self._on_action, _muself = Button._pop_myself(func)
        if _muself is False:
            myself = False
        self._on_action_args = ((self,) + args) if myself else args
        self._on_action_kwargs = kwargs
        _tmsg = f"on_action() ====\n"
        _tmsg += f"  {self._on_action=}\n"
        _tmsg += f"  {self._on_action_args=}\n"
        _tmsg += f"  {self._on_action_kwargs=}"
        Button._trace(7, _tmsg)

    def on_pressed(self, func, *args, myself=None, **kwargs):
        self._on_pressed, _muself = Button._pop_myself(func)
        self._on_pressed_args = ((self,) + args) if any([myself, _muself]) else args
        self._on_pressed_kwargs = kwargs
        _tmsg = f"on_pressed() ====\n"
        _tmsg += f"  {self._on_pressed=}\n"
        _tmsg += f"  {self._on_pressed_args=}\n"
        _tmsg += f"  {self._on_pressed_kwargs=}"
        Button._trace(7, _tmsg)

    def on_released(self, func, *args, myself=None, **kwargs):
        self._on_released, _muself = Button._pop_myself(func)
        self._on_released_args = ((self,) + args) if any([myself, _muself]) else args
        self._on_released_kwargs = kwargs
        _tmsg = f"on_released() ====\n"
        _tmsg += f"  {self._on_released=}\n"
        _tmsg += f"  {self._on_released_args=}\n"
        _tmsg += f"  {self._on_released_kwargs=}"
        Button._trace(7, _tmsg)

    def on_held(self, func, *args, myself=None, **kwargs):
        self._on_held, _muself = Button._pop_myself(func)
        self._on_held_args = ((self,) + args) if any([myself, _muself]) else args
        self._on_held_kwargs = kwargs
        _tmsg = f"held() ====\n"
        _tmsg += f"  {self._on_held=}\n"
        _tmsg += f"  {self._on_held_args=}\n"
        _tmsg += f"  {self._on_held_kwargs=}"
        Button._trace(7, _tmsg)


# ---------------------------- LED class  below ----------------------------------------------
class Mu():
    ''' Instant Closure クラス '''
    def __init__(self, func, *args, **kwargs):
        ''' 普通の関数(func)をクロージャーとして埋め込むクラスの MicroPythonバージョン
        '''
        # 仕様は functools.partial() とほとんど同じ（多分）だけど、
        # 埋め込んだ functionを呼び出すときの位置引数の順番が逆
        # （呼び出し時の引数が先、埋め込んだ引数が後）
        # あと、functools.partial()は MicroPythonで使えなかった。

        self.args = args
        self.kwargs = kwargs
        self.func = func

    def __call__(self, *args2, **kwargs2):
        return self.func(*args2, *self.args, **dict(**self.kwargs, **kwargs2))
        # return self.func(*args2, *self.args, {**self.kwargs, **kwargs2})
    

class LED(Signal):
    ''' LEDクラス（Signalのサブクラス） '''
    def __init__(self, pno, value=0, invert=False):
        self._notinvert = not invert
        super().__init__(Pin(pno, Pin.OUT), invert=invert)
        self.value(value)
        self._background = None

    def stop_background(self, sync=True):
        ''' blink などのバックグラウンド処理を停止する '''
        if self._background:
            self._background.cancel(sync=False)
            self._background = None

    def stop_background_and_execute(self, func, sync=True):
        ''' blink などのバックグラウンド処理を停止した後 func を実行する '''
        if self._background:
            Edas(Edas.y_oneshot(func), previous_task=self._background)
            self._background.cancel(sync=False)
        else:
            func()

    def on(self, within=None):
        ''' LEDを点灯する '''
        self.stop_background_and_execute(super().on, sync=False)

    def on_for(self, seconds=0.5):
        ''' LEDを点灯し、seconds秒後に消灯する '''
        self.stop_background_and_execute(super().on)
        if seconds > 0.0:
            self._background = Edas.after(seconds, super().off)

    def off(self):
        ''' LEDを消灯する '''
        self.stop_background_and_execute(super().off, sync=False)

    def toggle(self):
        ''' LEDの点灯と消灯を切り替える '''
        self.value(1-self.value())


    def y_blink(self, on_time, off_time, n):
        # print(f"y_blink {on_time=} {off_time=}")
        _ctime = CheckTime()
        _count = 0
        _on_time = round(on_time * 1000)
        _off_time = round(off_time * 1000)
        # _interval = _on_time + _off_time
        # print(f"y_blink {_on_time=} {_off_time=} {_interval=}")
        try:
            while not n or _count < n:
                self.value(1)
                yield from _ctime.y_wait_ms(_on_time, update=True)
                self.value(0)
                # yield from _ctime.y_wait(_interval)
                yield from _ctime.y_wait_ms(_off_time, update=True)
                yield Edas.SYNC
                _count += 1
                # _ctime.add_ms(_interval)
        except GeneratorExit as e:  # 途中で close()された場合
            self.value(0)

    def blink(self, on_time=1.0, off_time=1.0, n=None, followto=None):
        ''' LEDを点滅させる '''
        if self._background:
            self._background.cancel()
        self._background = Edas(self.y_blink(on_time, off_time, n), previous_task=followto,
                                terminate_by_sync=True)
        return self._background

    def flicker(self, interval=1.0, duty=0.5, n=None, followto=None):
        ''' LEDを点滅させる（blinkと引数の指定方法が違うだけ） '''
        _on_time = interval * duty
        _off_time = interval - _on_time
        if self._background:
            self._background.cancel()
        self._background = Edas(self.y_blink(_on_time, _off_time, n), previous_task=followto,
                                terminate_by_sync=True)
        return self._background


class PWMLED(PWM):
    ''' LEDを PWMを用いて制御するクラス（PWMのサブクラス） '''
    def __init__(self, pin, freq=100, value=0.0, lo=0.0, hi=1.0, invert=False, curve=1.0):
        if type(pin) is int:        # 番号で指定された
            self._pin = Pin(pin, Pin.OUT, value=0)
        elif type(pin) is LED:      # LED()で指定された
            self._pin = pin
        else:                       # それ以外（多分 Pin）
            self._pin = pin

        super().__init__(self._pin, freq=freq, invert=invert)

        self.curve = curve
        self.lo = max(min(lo, 1.0), 0)
        self.hi = max(min(hi, 1.0), self.lo)
        self._background = None

        self.value(value)

    def stop_background(self, sync=False):
        ''' blinkや fadeinなどのバックグラウンド処理を停止する '''
        if self._background:
            self._background.cancel(sync)
            self._background = None

    def stop_background_and_execute(self, func, sync=False):
        ''' blinkや fadeinなどのバックグラウンド処理を停止した後 func を実行する '''
        if self._background:
            ret = Edas(Edas.y_oneshot(func), previous_task=self._background)
            self._background.cancel(sync)
        else:
            ret = func()
        return

    def value(self, value=None):
        ''' PWMの duty比率を value の値で設定／取得する '''
        return self.duty(value)

    def duty(self, value=None):
        ''' PWMの duty比率を 0.0～1.0 の範囲で設定／取得する '''
        if value is None:
            ret = self.duty_u16() / 65535
            ret = ret ** (1.0/self.curve)
            return ret
        else:
            value = min(max(0.0, value), 1.0)
            _value=value ** self.curve
            self.duty_u16(round(65535 * _value))
            return value

    def y_fade(self, fade_time, duty_from, duty_to):
        # print(f"y_fade, {fade_time=} {duty_from=} {duty_to=}")
        if fade_time < 0.1:
            self.duty(duty_to)
            return
        ftime = fade_time * 1000
        duty_span = duty_to - duty_from
        spoint = time.ticks_ms()
        _wratio = 0
        while _wratio < 1.0:
            _wratio = (time.ticks_ms() - spoint) / ftime
            _wduty = _wratio * duty_span + duty_from
            self.duty(_wduty)
            yield
        self.duty(duty_to)

    def _fade(self, fade_time, duty_from=0.0, duty_to=1.0):
        self._background = Edas(self.y_fade(fade_time, duty_from, duty_to))
        return self._background

    def fadein(self, fade_time=1):
        ''' PWMの duty比を現在値から 最高値まで fade_time秒かけて変化させる '''
        if self._background:
            self._background.cancel()
        return self._fade(fade_time, self.duty(), self.hi)

    def fadeout(self, fade_time=1):
        ''' PWMの duty比を現在値から 最低値まで fade_time秒かけて変化させる '''
        if self._background:
            self._background.cancel()
        return self._fade(fade_time, self.duty(), self.lo)

    def _on(self):
        ''' PWMLEDをフル点灯する（duty比を最高値にする） '''
        self.duty(self.hi)
    
    def _off(self):
        ''' PWMLEDを消灯する（duty比を最低値にする） '''
        self.duty(self.lo)

    def on(self):
        ''' PWMLEDをバックグラウンド処理停止後、フル点灯する（duty比を最高値にする） '''
        self.stop_background_and_execute(self._on, sync=False)

    def off(self):
        ''' PWMLEDをバックグラウンド処理停止後、消灯する（duty比を最低値にする） '''
        self.stop_background_and_execute(self._off, sync=False)

    def y_blink(self, on_time, off_time, fade_in_time, fade_out_time, n):
        # print(f"{on_time=}, {off_time=}, {fade_in_time=}, {fade_out_time=}, {n=}")
        if fade_in_time > on_time:
            fade_in_time = on_time - 0.1
        if fade_out_time > on_time - fade_in_time:
            fade_out_time = on_time - fade_in_time - 0.1
        _point1 = round((on_time - fade_out_time) * 1000)
        _point2 = round((on_time + off_time) * 1000)
        _ctime = CheckTime()
        _count = 0
        try:
            while not n or _count < n:
                yield from self.y_fade(fade_in_time, self.lo, self.hi)
                yield from _ctime.y_wait_ms(_point1)
                yield from self.y_fade(fade_out_time, self.hi, self.lo)
                yield from _ctime.y_wait_ms(_point2)
                yield Edas.SYNC
                _ctime.add_ms(_point2)
                _count += 1
        except GeneratorExit as e:  # 途中で close()された場合
            self._off()

    def blink(self, on_time=1.0, off_time=1.0, fade_in_time=0.0, fade_out_time=0.0, n=None):
        ''' PWMLEDを点滅させる。点灯時、点灯終了時にfadein/fadeoutを行う '''
        if self._background:
            self._background.cancel()
        self._background = Edas(self.y_blink(on_time, off_time, fade_in_time, fade_out_time, n),
                                name="blink", terminate_by_sync=True)
        return self._background

    def y_pulse(self, fade_in_time, fade_out_time, n):
        _count = 0
        try:
            while not n or _count < n:
                yield from self.y_fade(fade_in_time, self.lo, self.hi)
                yield from self.y_fade(fade_out_time, self.hi, self.lo)
                yield Edas.SYNC
                _count += 1
        except GeneratorExit as e:  # 途中で close()された場合
            self._off()

    def pulse(self, fade_in_time=1.0, fade_out_time=1.0, n=None):
        ''' PWMLEDを連続して点滅させる。点滅時にfadein/fadeoutを行う '''
        if self._background:
            self._background.cancel()
        self._background = Edas(self.y_pulse(fade_in_time, fade_out_time, n), name="pulse",
                                terminate_by_sync=True)
        return self._background

    def _toggle(self):
        self.duty(1 - self.duty())

    def toggle(self):
        ''' 現在の duty比を逆転する '''
        self._toggle()


if __name__ == '__main__':
    def blink(led, ontime, offtime, n):
        _ctime = CheckTime()
        _count = 0
        while not n or _count < n:
            print(f"ON at  {time.ticks_ms()}")
            led.on()
            yield from _ctime.y_wait_ms(ontime, update=True)
            print(f"Off at {time.ticks_ms()}")
            led.off()
            yield from _ctime.y_wait_ms(offtime, update=True)
            print(f"end at {time.ticks_ms()}")
            yield Edas.SYNC
            _count += 1
        return "**OWARIDAYO**"


    print(__doc__)
    print(f"version = {__version__}")

    led1 = LED(16)
    led2 = LED(17)
    task1 = Eloop.create_task(blink(led1, 1000, 1000, 5), name="task1", terminate_by_sync=True)
    task2 = Eloop.create_task(blink(led2, 800, 400, 5), name="task2", previous_task=task1, terminate_by_sync=True)
    # Eloop.start()
    Eloop.start(tracelevel=11, loop_interval=100, id=0)
    bloop = Button.start(pull_up=True, tracelevel=12, period=100)

    led_0 = LED("LED")
    btn_0 = Button(Bootsel_button(), name="Bootsel_button", hold_time=1.0,
                    on_released=Mu(led_0.flicker, duty=0.8),
                    on_held=led_0.off
                    )

    for i in range(1000):
        # with Eloop.Suspender():
        print(f"---- round {i} ----")
        print(f"{Button.idle_time()=}")
        print(f"{Edas._get_taskcount()=}")
        print(f"{Edas._get_taskcount(Edas.BASIC)=}")
        print(f"{Eloop.idle_time()=}")
        if Button.idle_time() > 30.0:
            break
        time.sleep_ms(3000)

    Eloop.cancel_tasks()
    Eloop.wait_for_idle()

    print(f"{task1.done()=}")
    print(f"{task1.result()=}")
    print(f"{task2.done()=}")
    print(f"{task2.result()=}")

    print()
    print(f"name ={task1.name}")
    print(f"start={task1._start_point}")
    print(f"end  ={task1._end_point}")
    print(f"lifetime={time.ticks_diff(task1._end_point, task1._start_point):,}")
    print(f"name ={task2.name}")
    print(f"start={task2._start_point}")
    print(f"end  ={task2._end_point}")
    print(f"lifetime={time.ticks_diff(task2._end_point, task2._start_point):,}")
