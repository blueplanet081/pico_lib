from machine import Pin
from e_module import Edas, CheckTime

def lblink(pin, on_time, off_time, n):
    ctime = CheckTime()
    count = 0
    while not n or count < n:
        pin.value(1)
        yield from ctime.y_wait(on_time, update=True)
        pin.value(0)
        yield from ctime.y_wait(off_time, update=True)
        count += 1

led = Pin("LED", Pin.OUT)
Edas.loop_start()
Edas(lblink(led, 1000, 500, 5))

Edas.wait_for_idle()
