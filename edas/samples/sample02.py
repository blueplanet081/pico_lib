'''
sample02.py
- LEDクラスの使用方法いろいろ
'''
import time
from e_machine import Eloop, LED, Button, Mu

if __name__ == '__main__':
    class flickers():
        def __init__(self, led: LED):
            self.led = led
            self.interval = 0
            self.pfast = False
            self.pslow = False

        def fast(self, myself):
            if myself.reason == 1:      # pressed
                self.pfast = True
                if all([self.pfast, self.pslow]):   # 
                    self.interval = 0
                    self.led.off()
                else:
                    if self.interval == 0:
                        self.interval = 1
                    else:
                        self.interval /= 2
                    self.led.flicker(interval=self.interval)
            else:                       # released
                self.pfast = False

        def slow(self, myself):
            if myself.reason == 1:      # pressed
                self.pslow = True
                if all([self.pfast, self.pslow]):
                    self.interval = 0
                    self.led.off()
                else:
                    if self.interval == 0:
                        self.interval = 1
                    else:
                        self.interval *= 2
                    self.led.flicker(interval=self.interval)
            else:                       # released
                self.pslow = False

    # Edas.start_loop(tracelevel=18, period=10)
    Eloop.start(tracelevel=18, loop_interval=10)
    bloop = Button.start(pull_up=True, tracelevel=0, period=100)

    led_R = LED(16)     # 赤LED
    led_G = LED(17)     # 青LED
    led_Y = LED(18)     # 黄LED
    # led_B = LED(19, invert=True)    # 青LED

    BTN_A = const(14)
    BTN_B = const(15)
    # BTN_C = const(4)
    # BTN_D = const(5)
    # BTN_E = const(6)
    # BTN_F = const(7)

    # btn_A を押すと led_Rを点滅、長押しで消灯
    btn_A = Button(BTN_A, name="Btn_A", hold_time=1.0,
                   on_released=Mu(led_R.blink, on_time=1.0, off_time=0.2),
                   on_held=led_R.stop_background
                   )

    # btn_B を押すと led_Gを点滅、長押しで消灯（blink の代わりに flickerを使用）
    btn_B = Button(BTN_B, name="Btn_B", hold_time=1.0,
                   on_released=Mu(led_G.flicker, interval=1.5, duty=0.8),
                   on_held=led_G.stop_background
                   )

    # # btn_C で led_Yを 5秒間点灯、押すたびに延長、btn_D で即消灯
    # btn_C = Button(BTN_C, name="Btn_C", on_pressed=Mu(led_Y.on, within=5))
    # btn_D = Button(BTN_D, name="Btn_D", on_pressed=led_Y.off)


    # # btn_E で led_Bを点滅早、btn_F で点滅遅、同時押しで消灯
    # flick_B = flickers(led_B)
    # btn_E = Button(BTN_E, pull_up=False, name="Btn_E", on_action=flick_B.fast)
    # btn_F = Button(BTN_F, pull_up=False, name="Btn_F", on_action=flick_B.slow)

    for i in range(200):
        print(f"---- round {i} ----")
        if Eloop.idle_time() > 20:
            break
        time.sleep_ms(3000)
