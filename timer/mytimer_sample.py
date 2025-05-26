import rp2
import time

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


if __name__ == '__main__':
    # コールバック関数
    def callback1(timer):
        tm = time.ticks_ms()
        print(f"-> PIO triggered callback! {tm=}")


    timer1 = MyTimer(0)
    timer1.init(callback=callback1, period=1000, mode=MyTimer.PERIODIC)

    for i in range(5):
        print(f"---- round {i} ----")
        print(f"{time.ticks_ms()=}")
        time.sleep(10)



