from machine import Pin
from e_module import Edas, CheckTime

morse_data = {
    'a': (0b01, b'\x02'),
    'b': (0b1000, b'\x04'),
    'c': (0b1010, b'\x04'),
    'd': (0b100, b'\x03'),
    'e': (0b0, b'\x01'),
    'f': (0b0010, b'\x04'),
    'g': (0b110, b'\x03'),
    'h': (0b0000, b'\x04'),
    'i': (0b00, b'\x02'),
    'j': (0b0111, b'\x04'),
    'k': (0b101, b'\x03'),
    'l': (0b0100, b'\x04'),
    'm': (0b11, b'\x02'),
    'n': (0b10, b'\x02'),
    'o': (0b111, b'\x03'),
    'p': (0b0110, b'\x04'),
    'q': (0b1101, b'\x04'),
    'r': (0b010, b'\x03'),
    's': (0b000, b'\x03'),
    't': (0b1, b'\x01'),
    'u': (0b001, b'\x03'),
    'v': (0b0001, b'\x04'),
    'w': (0b011, b'\x03'),
    'x': (0b1001, b'\x04'),
    'y': (0b1011, b'\x04'),
    'z': (0b1100, b'\x04'),

    '0': (0b11111, b'\x05'),
    '1': (0b01111, b'\x05'),
    '2': (0b00111, b'\x05'),
    '3': (0b00011, b'\x05'),
    '4': (0b00001, b'\x05'),
    '5': (0b00000, b'\x05'),
    '6': (0b10000, b'\x05'),
    '7': (0b11000, b'\x05'),
    '8': (0b11100, b'\x05'),
    '9': (0b11110, b'\x05'),

    '.': (0b010101, b'\x06'),
    ',': (0b110011, b'\x06'),
    '?': (0b001100, b'\x06'),
    "'": (0b011110, b'\x06'),
    '!': (0b101011, b'\x06'),
    '/': (0b10010, b'\x05'),
    '(': (0b10110, b'\x05'),
    ')': (0b101101, b'\x06'),
    '&': (0b01000, b'\x05'),
    ':': (0b111000, b'\x06'),
    ';': (0b101010, b'\x06'),
    '=': (0b10001, b'\x05'),
    '+': (0b01010, b'\x05'),
    '-': (0b100001, b'\x06'),
    '_': (0b001101, b'\x06'),
    '"': (0b010010, b'\x06'),
    '$': (0b0001001, b'\x07'),
    '@': (0b011010, b'\x06'),

    'SOS': (0b000111000, b'\x09'),
    'AR': (0b01010, b'\x05'),
    'BT': (0b10001, b'\x05'),
    'KN': (0b101101, b'\x06'),
    'SK': (0b000101, b'\x06'),

    # --- 主要なプロサイン (Prosigns) と略語 (通常、スペースなしで送信) ---
    'HH': (0b00000000, b'\x08'),    # 訂正
    'BT': (0b10001, b'\x05'),       # -...- (区切り/改行 - Break)／送信開始？
    'AR': (0b01010, b'\x05'),       # .-.-. (メッセージの終わり - End of Message)／送信終了？
    'VA': (0b000101, b'\x06'),      # ...-.- (交信終了 - End of contact/signing off) - Note: Same as SK
                                    # VA is often used formally for "End of Work/Transmission"
                                    # While SK implies ending a specific QSO.
                                    # Here, defined same as SK as it's often used interchangeably.
    'K': (0b101, b'\x03'),          # -.- (どうぞ - Go ahead) - Note: Same as 'K' alphabet／送信要求
    'AS': (0b01000, b'\x05'),       # 待機要求
    'SN': (0b00010, b'\x05'),       # 了解

    'SOS': (0b000111000, b'\x09'),  # ...---... (遭難信号 - Distress Call)
    'CL': (0b10100100, b'\x08'),    # -.-. .-.. (送信終了 - Closing station)
    'CQ': (0b1011101, b'\x07'),     # -.-. --.- (不特定の局への呼び出し - Calling any station)
    'DE': (0b1000, b'\x04'),        # -.. . (～から - From)
    'KN': (0b101101, b'\x06'),      # -.-.-- (特定の局へどうぞ - Go ahead only)
    'R': (0b010, b'\x03'),          # .-. (了解/受信済み - Roger / Received) - Note: Same as 'R' alphabet
    'SK': (0b000101, b'\x06'),      # ...-.- (交信終了 - End of contact/signing off)
    'TU': (0b001, b'\x03'),         # ..- (ありがとう - Thank you) - Note: Same as 'U' alphabet
}

def get_morse_string(char):
    ''' 文字コードから、ドットとダッシュを 01で表す符号文字列を取得する '''
    char = char.lower()
    if char in morse_data:
        data, len = morse_data[char]
        ret = f"{bin(data)[2:]:>0{int.from_bytes(len)}}"
        return ret
    else:
        return ""

def morse_unit_duration(wpm:float):
    """
    WPM（Words Per Minute）を元に、モールス信号の1単位（ドット）の長さを秒で返す。
    PARIS基準（1語 = 50単位）に基づく。
    """
    if wpm <= 0:
        raise ValueError("WPM must be a positive value.")
    
    units_per_minute = wpm * 50     # 1語 = 50単位
    unit_duration = 60 / units_per_minute   # 単位秒数
    return unit_duration

def blink_led_morse(led, char, ud=1.2):
    code_string = get_morse_string(char)
    print(f"{char=}, {code_string=}, {ud=}")
    if code_string:
        for char in code_string:
            if char == '0':
                led.on()
                yield from Edas.y_sleep(ud)
                led.off()
                yield from Edas.y_sleep(ud)
            else:
                led.on()
                yield from Edas.y_sleep(ud * 3)
                led.off()
                yield from Edas.y_sleep(ud)
    else:
        yield from Edas.y_sleep(ud*2)
    yield from Edas.y_sleep(ud*2)
    yield Edas.SYNC

def blink_led_mourse_string(led, string, wpm=10.0):
    ut = morse_unit_duration(wpm)
    t = None
    for char in string:
        t = Edas(blink_led_morse(led, char, ud=ut))
        while not t.done():
            yield
    print()


led = Pin("LED", Pin.OUT)
led1 = Pin(16, Pin.OUT)
led2 = Pin(17, Pin.OUT)
led3 = Pin(18, Pin.OUT)

Edas.loop_start(tracelevel=0)

Edas(blink_led_mourse_string(led, "sos sos sos"))
Edas(blink_led_mourse_string(led1, "sos sos", wpm=5))
Edas(blink_led_mourse_string(led2, "sos sos sos sos", wpm=15))
Edas(blink_led_mourse_string(led3, "Raspberry Pi Pico", wpm=12), on_cancel=led1.on)
Edas(Edas.y_sleep(1))
Edas.wait_for_idle()

