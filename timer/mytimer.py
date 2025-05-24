import rp2
import time

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

gcount = 0

# コールバック関数
def my_callback(timer):
    global gcount
    tm = time.ticks_ms()
    print(f"{gcount} triggered callback! {tm=}")
    gcount += 1
    time.sleep_ms(50)

def my_callback2(timer):
    tm = time.ticks_ms()
    print(f"-> PIO triggered callback! {tm=}")

timer = MyTimer(0)
timer2 = MyTimer(1)

# rate=1000だと、1,000msec毎に my_callbackが呼び出される
timer.init(callback=my_callback, period=100, mode=MyTimer.PERIODIC)

for i in range(5):
    print(f"---- round {i} ----")
    print(f"{time.ticks_ms()=}")
    # timer2.init(callback=my_callback2, period=1000, mode=MyTimer.ONE_SHOT)
    time.sleep(10)

# sm.active(0)  # ステートマシンを無効化
time.sleep(10)


