'''
sample_async_00.py
asyncと協調テスト
- Pico W 本体のLEDとボタンの操作
  - プログラム開始時に LEDを 3回点滅させる
  - ボタンを押して点滅開始、ボタン長押しで消灯
  - ボタンを 20秒以上操作しないと、LEDを消灯してプログラム終了
'''
import time
from edas2.e_module2 import Edas
from e_machine import Eloop, Button, Bootsel_button, LED

# Eloop.start(loop_interval=10, tracelevel=14)
Eloop.start(loop_interval=10, tracelevel=0)
bloop = Button.start(period=100, tracelevel=0)

led_0 = LED("LED")
led_0.flicker(0.5, 0.5, 3)
btn_0 = Button(Bootsel_button(), name="Bootsel_button", hold_time=1.0,
                on_released=led_0.flicker,
                on_held=led_0.off
                )

import asyncio
# from e_machine import Eloop, LED

async def blink(led, period_ms):
    while True:
        led.on()
        # await asyncio.sleep_ms(10)
        await asyncio.sleep(0.2)
        led.off()
        await asyncio.sleep_ms(period_ms)

async def main(led1, led2):
    asyncio.create_task(blink(led1, 700))
    asyncio.create_task(blink(led2, 400))
    tt = asyncio.current_task()
    print(dir(tt))
    await asyncio.sleep_ms(50_000)

# la = LED(16)
# Eloop.start(id=0)
# la.blink()


from machine import Pin, Signal
l1 = Signal(16, Pin.OUT)
l2 = Signal(17, Pin.OUT)
asyncio.run(main(l1, l2))


i = 0
while True:
    if Button.idle_time() > 20.0:
        led_0.off()
        Eloop.cancel_basic_tasks()
        Eloop.wait_for_idle()
        break

    print(f"---- round {i} ----")
    i += 1
    time.sleep_ms(1000)

Edas.show_edas()
