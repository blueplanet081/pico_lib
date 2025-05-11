'''
sample00.py
- Pico W 本体のLEDとボタンの操作
  - プログラム開始時に LEDを 3回点滅させる
  - ボタンを押して点滅開始、ボタン長押しで消灯
  - ボタンを 20秒以上操作しないと、LEDを消灯してプログラム終了
'''
import time
from e_module import Edas
from e_machine import Eloop, Button, Bootsel_button, LED

# Eloop.start(loop_interval=10, tracelevel=14)
Eloop.start(loop_interval=10, tracelevel=11)
bloop = Button.start(period=100, tracelevel=11)

led_0 = LED("LED")
led_0.flicker(0.5, 0.5, 3)
btn_0 = Button(Bootsel_button(), name="Bootsel_button", hold_time=1.0,
                on_released=led_0.flicker,
                on_held=led_0.off
                )

i = 0
while True:
    if Button.idle_time() > 20.0:
        # print("offff!!")
        led_0.off()
        Eloop.cancel_basic_tasks()
        Edas.show_edas()
        Eloop.wait_for_idle()
        Edas.show_edas()
        break

    print(f"---- round {i} ----")
    i += 1
    time.sleep_ms(1000)

Edas.show_edas()
Edas.show_edas()
Edas.show_edas()
Edas.show_edas()
