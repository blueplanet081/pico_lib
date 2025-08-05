'''
sample01.py
- Buttonの使用方法いろいろ
'''
import time
from e_machine import Eloop, Button, LED

def testM(myself):
    print(f"on_action <{myself.name}> {myself.reason=}" +
                f"({Button.str_reason(myself.reason)})")
    print(f"{myself.count=}")           # 押された回数
    print(f"{myself.repeat_count=}")    # repeatされた回数
    print(f"{myself.interval_time=}")   # 押された間隔(msec)
    print(f"{myself.active_time=}")     # 押されていた時間(msec)
    print(f"{myself.inactive_time=}")   # 離されていた時間(msec)


Eloop.start(loop_interval=10)
bloop = Button.start(tracelevel=10, period=100)

led_R = LED(16)     # 赤LED
led_B = LED(17)     # 青LED

BTN_A = const(14)
BTN_B = const(15)

# btn_A を押して led_Rを点灯、離して消灯
btn_A = Button(BTN_A, name="Btn_A",
               on_pressed=led_R.on,
               on_released=led_R.off)

# btn_B を押して離して led_Bを点灯、2秒以上長押しで消灯
btn_B = Button(BTN_B, name="Btn_B", hold_time=2.0,
               on_released=led_B.on,
               on_held=led_B.off)

for i in range(50):
    print(f"---- round {i} ----")
    time.sleep_ms(3000)
