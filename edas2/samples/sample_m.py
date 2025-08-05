import time
from e_module import Edas
from e_machine import Eloop, Button, Bootsel_button, LED, Mu, PWMLED

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
    if char in morse_data:
        data, len = morse_data[char]
        ret = f"{bin(data)[2:]:>0{int.from_bytes(len)}}"
        return ret
    else:
        print(f"unknown char: '{char}'")
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

def y_send_char(led, char, ut=0.12):
    ''' １文字分のモールス信号を出力するタスクジェネレータ '''
    code_string = get_morse_string(char)
    # print(f"{char=}, {code_string=}, {ut=}")
    if code_string:
        for char in code_string:
            if char == '0':     # . ドット
                led.on()
                yield from Eloop.y_sleep(ut)
                led.off()
                yield from Eloop.y_sleep(ut)
            else:               # - ダッシュ
                led.on()
                yield from Eloop.y_sleep(ut * 3)
                led.off()
                yield from Eloop.y_sleep(ut)
    else:
        yield from Eloop.y_sleep(ut*2)  # 空文字
    yield from Eloop.y_sleep(ut*2)  # 文字間スペース

def y_send_text(led, string, ut=0.12):
    ''' 一連のテキスト（文字列）のモールス信号を出力するタスクジェネレータ '''
    for char in string:
        print(f"{char=}")
        yield from y_send_char(led, char.lower(), ut=ut)
        yield Edas.SYNC

def y_send_prosign(led, psign, ut=0.12):
    ''' １文字分の特殊符号のモールス信号を出力するタスクジェネレータ '''
    yield from y_send_char(led, psign.upper(), ut=ut)
    yield Edas.SYNC


class MorseTransmitter():
    ''' テキストをモールス信号でled出力するクラス '''
    def __init__(self, led, wpm=10.0) -> None:
        self.wpm = wpm
        self.led = led
        self.ut = morse_unit_duration(wpm)
        self.tasklist = []
        self.tnum = 0

    def send_text(self, text):
        ''' テキストを送信する '''
        print(f"{text=}")
        ltask = None if not self.tasklist else self.tasklist[-1]
        self.ltask = Eloop.create_task(
            y_send_text(self.led, text, ut=self.ut), terminate_by_sync=True,
            previous_task=ltask, name=f"send{self.tnum:04}")
        
        self.tasklist.append(self.ltask)
        self.tnum += 1

    def send_prosign(self, psign):
        ''' 特殊符号を送信する '''
        print(f"{psign=}")
        ltask = None if not self.tasklist else self.tasklist[-1]
        self.ltask = Eloop.create_task(
            y_send_prosign(self.led, psign, ut=self.ut), terminate_by_sync=True,
            previous_task=ltask, name=f"send{self.tnum:04}")
        
        self.tasklist.append(self.ltask)
        self.tnum += 1

    def cancel(self):
        ''' 送信を中止する '''
        while self.tasklist:
            wtask = self.tasklist.pop(0)
            if not wtask.done():
                print(f"{wtask.name=}")
                wtask.cancel(sync=True)


led = LED("LED")
led1 = LED(16)
led2 = LED(17)

led3 = PWMLED(18)

BTN_A = const(13)
BTN_B = const(14)
BTN_C = const(15)

mt0 = MorseTransmitter(led, wpm=8)
mt1 = MorseTransmitter(led1, wpm=15)
mt2 = MorseTransmitter(led2, wpm=20)

Eloop.start(tracelevel=21)
Button.start()

for _ in range(10):
    mt0.send_prosign("SOS")
btn_0 = Button(Bootsel_button(), on_pressed=mt0.cancel) 

for _ in range(10):
    mt2.send_prosign("SOS")

btn_A = Button(BTN_A, name="Btn_A", on_pressed=Mu(mt1.send_text, "Raspberry Pi Pico W") )
btn_B = Button(BTN_B, name="Btn_B", on_pressed=mt1.cancel)

btn_C = Button(BTN_C, name="Btn_C", hold_time=1.0,
               on_released=led3.pulse,
               on_held=led3.off)


for i in range(200):
    print(f"---- round {i} ----")
    if Eloop.idle_time() > 10:
        break
    time.sleep_ms(3000)
print("loopend")
