'''
sample03.py
- PWMLEDクラスの使用方法いろいろ
'''
import time
from micropython import const
from mymachine import Edas, PWMLED, LED, Button, Mu

class Volume():
    def __init__(self, pwmled: PWMLED, range=10, curve=1.0):
        pwmled.curve = curve
        self.pwmled = pwmled
        self.volume = 0.0
        self.step = 1 / range
        self.pup = False
        self.pdown = False

    def up(self, myself):
        if myself.reason in (1, 4):      # PRESSED or REPEATED
            self.pup = True
            if all([self.pup, self.pdown]):     # 同時押し判定 
                self.volume = 0.0
                self.pwmled.off()
            else:
                self.volume = min((self.volume + self.step), 1.0)
                self.pwmled.duty(self.volume)
        else:                       # released
            self.pup = False

    def down(self, myself):
        if myself.reason in (1, 4):      # PRESSED or REPEATED
            self.pdown = True
            if all([self.pup, self.pdown]):     # 同時押し判定
                self.volume = 0.0
                self.pwmled.off()
            else:
                self.volume = max(self.volume - self.step, 0.0)
                self.pwmled.duty(self.volume)
        else:                       # released
            self.pdown = False

class Blink():
    def __init__(self, pwmled: PWMLED):
        self.pwmled = pwmled
        self.interval = 0
        self.pfast = False
        self.pslow = False

    def fast(self, myself):
        if myself.reason == 1:      # pressed
            self.pfast = True
            if all([self.pfast, self.pslow]):       # 同時押し判定 
                self.interval = 0
                self.pwmled.off()
            else:
                if self.interval == 0:
                    self.interval = 1
                else:
                    self.interval /= 2
                self.pwmled.blink(self.interval, self.interval, self.interval/2, self.interval/2)
        else:                       # released
            self.pfast = False

    def slow(self, myself):
        if myself.reason == 1:      # pressed
            self.pslow = True
            if all([self.pfast, self.pslow]):       # 同時押し判定
                self.interval = 0
                self.pwmled.off()
            else:
                if self.interval == 0:
                    self.interval = 1
                else:
                    self.interval *= 2
                self.pwmled.blink(self.interval, self.interval, self.interval/2, self.interval/2)
        else:                       # released
            self.pslow = False


Edas.start_loop(tracelevel=0, period=10)
bloop = Button.start(pull_up=True, tracelevel=0, period=100)

led_R = PWMLED(16)      # 赤LED
led_G = PWMLED(17)      # 緑LED
led_Y = PWMLED(18)      # 黄LED
led_B = PWMLED(19, invert=True)     # 青LED

BTN_A = const(2)
BTN_B = const(3)
BTN_C = const(4)
BTN_D = const(5)
BTN_E = const(6)
BTN_F = const(7)


# btn_A を押すと点滅、長押しで消灯
btn_A = Button(BTN_A, name="Btn_A", hold_time=1.0,
                on_released=led_R.pulse,
                on_held=led_R.off
                )

# btn_C で明るく、btn_D で暗く、長押しでrepeat、　同時押しで消灯
vol_G = Volume(led_G, range=20, curve=1.5)
btn_C = Button(BTN_C, name="Btn_C", hold_time=0.5, repeat_time=0.1,
                on_action=vol_G.up)
btn_D = Button(BTN_D, name="Btn_D", hold_time=0.5, repeat_time=0.1,
                on_action=vol_G.down)

# btn_E で点滅早、btn_F で点滅遅、長押しでrepeat、同時押しで消灯
blink_Y = Blink(led_Y)
btn_E = Button(BTN_E, name="Btn_E", pull_up=False,
                on_action=blink_Y.fast)
btn_F = Button(BTN_F, name="Btn_F", pull_up=False,
                on_action=blink_Y.slow)


for i in range(200):
    print(f"---- round {i} ----")
    time.sleep_ms(3000)
