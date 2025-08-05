'''
sample04.py
- PWMLEDクラスの使用方法いろいろ
  （curve の効果のデモ）
'''
import time
from micropython import const
from mymachine import Edas, Button, Mu, PWMLED


def all_pressed(btns):
    with Edas.Freezed():
        for btn in btns:
            btn._on_pressed(*btn._on_pressed_args, **btn._on_pressed_kwargs)

def all_held(btns):
    for btn in btns:
        btn._on_held(*btn._on_held_args, **btn._on_held_kwargs)


Edas.start_loop(tracelevel=19, period=50)
bloop = Button.start(pull_up=True, tracelevel=12, period=100)

led_R = PWMLED(16, curve=0.5)   # 赤LED
led_G = PWMLED(17)              # 緑LED
led_Y = PWMLED(18, curve=2)     # 黄LED
led_B = PWMLED(19, invert=True, curve=4, lo=0.2, hi=0.8)    # 青LED

BTN_A = const(2)
BTN_B = const(3)
BTN_C = const(4)
BTN_D = const(5)
BTN_E = const(6)
BTN_F = const(7)


# btn_A ～ btn_Dを押して、各LEDの点滅開始、長押しで終了
btn_A = Button(BTN_A, name="Btn_A", hold_time=0.5,
                on_pressed=led_R.pulse,
                on_held=led_R.off
                )

btn_B = Button(BTN_B, name="Btn_B", hold_time=0.5,
                on_pressed=led_G.pulse,
                on_held=led_G.off
                )

btn_C = Button(BTN_C, name="Btn_C", hold_time=0.5,
                on_pressed=led_Y.pulse,
                on_held=led_Y.off
                )

btn_D = Button(BTN_D, name="Btn_D", hold_time=0.5,
                on_pressed=led_B.pulse,
                on_held=led_B.off
                )


# btn_Eを押して、全LEDの点滅を一斉に開始
btn_E = Button(BTN_E, name="Btn_E", pull_up=False,
                on_pressed=Mu(all_pressed, [btn_A, btn_B, btn_C, btn_D])
                )

# btn_Fを押して、全LEDの点滅を一斉に終了
btn_F = Button(BTN_F, name="Btn_F", pull_up=False,
                on_pressed=Mu(all_held, [btn_A, btn_B, btn_C, btn_D])
                )


for i in range(1000):
    print(f"---- round {i} ----")
    time.sleep_ms(3000)
