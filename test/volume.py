from machine import Pin, PWM, ADC
import time

SERVO_PIN = 27
PWM_FREQ = 50

def pulse_width( val, freq = PWM_FREQ, resol = 65535 ):
    pulse = freq * val * 1e-6 * resol
    return int( pulse )

servo = PWM( Pin( SERVO_PIN ) )
servo.freq( PWM_FREQ )

class Survo():
    def __init__(self, pwm_freq=50, min_duty = 0.6, max_duty = 2.6) -> None:
        self.pwm_freq = pwm_freq



MAX_VALUE = 65535
MIN_VALUE = 224
SCALE = MAX_VALUE - MIN_VALUE

class Volume:
    def __init__(self, gpio, max_value=65535, min_value=0) -> None:
        self.max_value = max_value
        self.min_value = min_value
        self.scale = self.max_value - self.min_value

        self.port_adc = ADC(Pin(gpio))

    def get_value(self):
        _value = self.port_adc.read_u16()
        return max(0, min((_value - self.min_value) / self.scale, 1.0))

port_adc = Volume(26, min_value = 250)


while True:
    # adc_value = port_adc.read_u16()
    # print(adc_value)

    # percentage = ((adc_value - MIN_VALUE) / SCALE) * 100
    percentage = port_adc.get_value()
    print(f"{percentage * 100:.2f}%")

    time.sleep(0.5)
