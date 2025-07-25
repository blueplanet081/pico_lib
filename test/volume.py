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



# MAX_VALUE = 65535
# MIN_VALUE = 224
# SCALE = MAX_VALUE - MIN_VALUE

class Volume:
    def __init__(self, gpio, max_value=65535, min_value=255) -> None:
        self.max_value = max_value
        self.min_value = min_value
        self.scale = self.max_value - self.min_value

        self.port_adc = ADC(Pin(gpio))

    def get_value(self):
        _value = self.port_adc.read_u16()
        return max(0, min((_value - self.min_value) / self.scale, 1.0))


class Servo():
    def __init__(self,
                 gpio,                  # GPIO No.
                 pwm_freq=50,           # Duty cycle(Hz)
                 duty_min = 0.6,        # minimum positon(msec)
                 duty_max = 2.6,        # maximum positon(msec)
                 rotation_angle=180,    # rotation_angle
                 invert=False           # invert
                 ):

        self.servo = PWM(Pin(gpio))
        self.servo.freq(pwm_freq)
        print(f"{self.servo.freq()=}")

        self.pwm_freq = pwm_freq
        self.max_width = 1 / 50 * 1000
        print(f"{self.max_width=}")
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.duty_span = duty_max - duty_min   # spam of duty(msec)
        self.rotation_angle = rotation_angle
        self.invert = invert

    def rotate(self, ratio):
        print(f"{ratio=}")
        ratio = (1 - ratio) if self.invert else ratio
        duty = self.duty_min + self.duty_span * ratio
        self.servo.duty_u16( int(65535 * duty / self.max_width))

    def rotate_by_degree(self, degree):
        ratio = degree / self.rotation_angle
        self.rotate(ratio)

class ValueFilter:
    def __init__(self, threshhold, range=1) -> None:
        self.threshold = threshhold
        self.previous_value = None
        self.range = range

    def has_changed(self, value) -> bool:
        if self.previous_value is None:
            self.previous_value = value
            return True
        _threshhold = self.threshold * value / self.range
        print(f"{abs(value - self.previous_value)}")
        # print(f"{_threshhold:0.4f}")
        if abs(value - self.previous_value) >= self.threshold:
            self.previous_value = value
            return True
        else:
            return False


servo = Servo(21, duty_min=0.45, duty_max=2.45)
servo2 = Servo(22, duty_min=0.6, duty_max=2.5, invert=True)

port_adc = Volume(26)
port_adc2 = Volume(27)

vfilter = ValueFilter(threshhold=0.001)
vfilter2 = ValueFilter(threshhold=0.0001)

while True:
    # adc_value = port_adc.read_u16()
    # print(adc_value)

    # percentage = ((adc_value - MIN_VALUE) / SCALE) * 100
    ratio = port_adc.get_value()
    ratio2 = port_adc2.get_value()
    # print(f"{ratio=}")

    if vfilter.has_changed(ratio):
        servo.rotate(ratio)
    if vfilter2.has_changed(ratio2):
        servo2.rotate(ratio2)

    time.sleep(0.005)
