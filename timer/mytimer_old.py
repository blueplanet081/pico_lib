import rp2
import time
from machine import Timer

class MyTimer():
    ''' StateMachineを使ったタイマー制御クラス '''
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
        self.sm.irq(self.intercepter)


    def intercepter(self, sm):
        ''' タイマー制御用callback関数 '''
        if self._counter <= 0:
            self._counter = self._period
            if self._mode == MyTimer.ONE_SHOT:
                self.sm.active(0)   # ステートマシンを無効化
            if self._callback:
                self._callback(self)
        self._counter -= 1

    def init(self, mode=PERIODIC, period=10, callback=None):
        ''' タイマーを初期化する '''
        assert callable(callback), "callback must be a callable object."
        self._callback = callback

        self._mode = mode
        self._period = period
        self._counter = self._period

        self.sm.active(1)  # ステートマシンを有効化

    def deinit(self):
        self.sm.active(0)


if __name__ == '__main__':
    class Callbacks():
        def __init__(self, name="noname", mode=0, period=0):
            self.gcount = 0
            self.former_tm = time.ticks_ms()
            self.name = name
            self.mode = mode
            self.period = period

        def callback0(self, timer):
            ''' 順次実行形式 '''
            tm = time.ticks_ms()
            print()
            print(f"{self.gcount} [{self.name}] callback! {tm=} {time.ticks_diff(tm, self.former_tm)}")
            self.gcount += 1
            self.former_tm = tm

            # 遅延負荷
            j = 0
            for i in range(40000):
                j += i

            rt = time.ticks_diff(time.ticks_ms(), tm)
            timer.init(callback=self.callback0, period=(self.period - rt), mode=MyTimer.ONE_SHOT)

        def callback1(self, timer):
            ''' 定期実行形式 '''
            tm = time.ticks_ms()
            print(f"{self.gcount} [{self.name}] callback! {tm=} {time.ticks_diff(tm, self.former_tm)}")
            self.gcount += 1
            self.former_tm = tm

            # 遅延負荷
            j = 0
            for i in range(40000):
                j += i
            # time.sleep_ms(50)

    timer0 = MyTimer(0)     # MyTimer(0)
    timer1 = MyTimer(1)     # Mytimer(1)
    timer = Timer(-1)       # machine.Timer

    cb0 = Callbacks(name="cb0", mode=MyTimer.ONE_SHOT, period=1000)     # 順次実行
    cb1 = Callbacks(name="cb1")     # 定期実行
    tmr = Callbacks(name="TMR")     # 定期実行（machine.Timer）

    timer0.init(callback=cb0.callback0, period=1000, mode=MyTimer.ONE_SHOT)
    timer1.init(callback=cb1.callback1, period=1000, mode=MyTimer.PERIODIC)
    timer.init(callback=tmr.callback1, period=1000, mode=Timer.PERIODIC)


    for i in range(5):
        print(f"---- round {i} ----")
        print(f"{time.ticks_ms()=}")
        time.sleep(10)
