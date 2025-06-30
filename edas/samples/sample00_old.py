'''
sample00.py
- Pico W 本体のLEDとボタンの操作
- ボタン操作（長押し）
- LEDの点滅、消灯
'''
import time
from e_machine import Eloop, Button, Bootsel_button, LED

Eloop.start(loop_interval=10)
bloop = Button.start(period=100)

led_0 = LED("LED")
btn_0 = Button(Bootsel_button(), name="Bootsel_button", hold_time=1.0,
                on_released=led_0.flicker,
                on_held=led_0.off
                )

for i in range(50):
    print(f"---- round {i} ----")
    time.sleep_ms(3000)
