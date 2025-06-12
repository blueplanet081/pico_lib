from machine import Pin, PWM
import time

# SERVO_PIN = 27
# PWM_FREQ = 50

# def pulse_width( val, freq = PWM_FREQ, resol = 65535 ):
#     pulse = freq * val * 1e-6 * resol
#     return int( pulse )

# servo = PWM( Pin( SERVO_PIN ) )
# servo.freq( PWM_FREQ )

class Servo():
    def __init__(self, gpio, pwm_freq=50, duty_min = 0.6, duty_max = 2.6, rotation_angle=180) -> None:
        self.servo = PWM(Pin(gpio))
        self.servo.freq(pwm_freq)
        print(f"{self.servo.freq()=}")

        self.pwm_freq = pwm_freq
        self.max_width = 1 / 50 * 1000
        print(f"{self.max_width=}")
        self.duty_min = duty_min
        self.duty_max = duty_max
        self.duty_width = duty_max - duty_min

    def move(self, duty):
        print(duty)
        self.servo.duty_u16( int(65535 * duty / self.max_width))

    def move_by_degree(self, degree):
        print(duty)
        self.servo.duty_u16( int(65535 * duty / self.max_width))


servo = Servo(27)
servo2 = Servo(28)

while True:
    print("start")
    # duty = pulse_width( 1500 )
    servo.move( 1.5 )
    servo2.move( 1.5 )
    time.sleep( 1 )
    
    # duty = pulse_width( 500 )
    servo.move( 0.5 )
    servo2.move( 0.6 )
    # servo.move( 1000 )
    time.sleep( 1 )

    # duty = pulse_width( 1500 )
    servo.move( 1.5 )
    servo2.move( 1.5 )
    time.sleep( 1 )

    # duty = pulse_width( 2500 )
    servo.move( 2.5 )
    servo2.move( 2.5 )
    # servo.move( 2000 )
    time.sleep( 1 )

