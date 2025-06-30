'''
sample01.py
- Buttonの使用方法いろいろ
'''
import time
from mymachine import Edas, LED, Button

def testM(myself):
    print(f"on_action <{myself.name}> {myself.reason=}" +
                f"({Button.str_reason(myself.reason)})")
    print(f"{myself.count=}")           # 押された回数
    print(f"{myself.repeat_count=}")    # repeatされた回数
    print(f"{myself.interval_time=}")   # 押された間隔(msec)
    print(f"{myself.active_time=}")     # 押されていた時間(msec)
    print(f"{myself.inactive_time=}")   # 離されていた時間(msec)


Edas.start_loop(tracelevel=18, period=10)
bloop = Button.start(pull_up=True, tracelevel=0, period=100)

led_R = LED(16)     # 赤LED
led_G = LED(17)     # 緑LED
led_Y = LED(18)     # 黄LED
led_B = LED(19, invert=True)    # 青LED

BTN_A = const(2)
BTN_B = const(3)
BTN_C = const(4)
BTN_D = const(5)
BTN_E = const(6)
BTN_F = const(7)

# btn_A を押すたびに led_Rを点、滅
btn_A = Button(BTN_A, name="Btn_A", on_pressed=led_R.toggle)

# btn_B を押して離したときに led_Gを点灯、1.2秒以上長押しで消灯
btn_B = Button(BTN_B, name="Btn_B", hold_time=1.2,
                on_released=led_G.on,
                on_held=led_G.off,
                )

# btn_C を押すたびに led_Yを点、滅、2秒以上押し続けると 0.5秒毎に点、滅を繰り返す
btn_C = Button(BTN_C, name="btn_C", hold_time=2, repeat_time=0.5)
btn_C.on_pressed(led_Y.toggle)

# btn_TEST（btn_D） を押す、長押しでrepeat、離すで情報を REPL画面に出力
btn_TEST = Button(BTN_D, name="Btn_TEST", on_action=testM, repeat_time=0.5)

# btn_ON(btn_E) で点灯、btn_OFF(btn_F) で消灯
btn_ON = Button(BTN_E, name="Btn_ON", pull_up=False, on_pressed=led_B.on)
btn_OFF = Button(BTN_F, name="Btn_OFF", pull_up=False, on_pressed=led_B.off)

for i in range(200):
    print(f"---- round {i} ----")
    time.sleep_ms(3000)
