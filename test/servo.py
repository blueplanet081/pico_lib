from machine import Pin, PWM, ADC
import time


class Volume:
    ''' Picoの ADCポートを使用して可変抵抗器の値を取得するクラス '''
    def __init__(self, gpio, offset=256) -> None:
        self._port_adc = ADC(Pin(gpio))

        self._full_scale_adc_value = 65535
        self._offset = offset
        self._effective_range = self._full_scale_adc_value - self._offset

    def get_value(self):
        ''' 可変抵抗器の値を 0.0 - 1.0の範囲で取得する '''
        _value = self._port_adc.read_u16()
        return max(0, min((_value - self._offset) / self._effective_range, 1.0))


class Servo():
    ''' サーボモーターを制御するクラス '''
    def __init__(self,
                 gpio,                  # GPIO No.
                 pwm_freq=50,           # Duty cycle(Hz)
                 min_duty = 0.6,        # minimum positon duty(msec)
                 max_duty = 2.6,        # maximum positon duty(msec)
                 rotation_angle=180,    # rotation_angle(degree)
                 invert=False           # invert
                 ):

        self._servo = PWM(Pin(gpio))
        self._servo.freq(pwm_freq)

        # self.pwm_freq = pwm_freq
        # self.max_width = 1 / 50 * 1000
        # print(f"{self.max_width=}")
        self._min_duty = min_duty
        self._max_duty = max_duty
        self._duty_span = max_duty - min_duty   # span of duty(msec)
        self._rotation_angle = rotation_angle
        self._invert = invert

    def rotate(self, ratio):
        print(f"{ratio=}")
        ratio = (1 - ratio) if self._invert else ratio
        duty = self._min_duty + self._duty_span * ratio
        # self.servo.duty_u16( int(65535 * duty / self.max_width))
        self._servo.duty_ns(int(duty * 1000000))
        # ns = self.servo.duty_ns()
        # print(f"{duty=}, {ns=}")

    def rotate_by_degree(self, degree):
        ratio = degree / self._rotation_angle
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


servo = Servo(21, min_duty=0.45, max_duty=2.45)
servo2 = Servo(22, min_duty=0.6, max_duty=2.5, invert=True)

port_adc = Volume(26)
port_adc2 = Volume(27)

vfilter = ValueFilter(threshhold=0.001)
vfilter2 = ValueFilter(threshhold=0.0001)

while True:
    ratio = port_adc.get_value()
    ratio2 = port_adc2.get_value()

    if vfilter.has_changed(ratio):
        servo.rotate(ratio)
    if vfilter2.has_changed(ratio2):
        servo2.rotate(ratio2)

    time.sleep(0.5)
