'''
HT16K33経由、4桁7segment LED表示器用モジュール
2025/7/29
'''

from micropython import const

class MyHT16K33:
    ''' HT16K33に接続された 4桁7segment LEDディスプレイを操作するクラス '''
    DISPLAY_SETUP = const(0x80)
    BLINK_DISPLAYON = const(0x01)
    CMD_BRIGHTNESS = const(0xE0)
    OSCILATOR_ON = const(0x21)

    SEG_MAP = {' ': 0x00, '!': 0x86, '"': 0x22, '#': 0x7e, '$': 0x6d,
               '%': 0xd2, '&': 0x46, "'": 0x20, '(': 0x29, ')': 0x0b,
               '*': 0x21, '+': 0x70, ',': 0x10, '-': 0x40, '.': 0x80, '/': 0x52,

               '0': 0x3F, '1': 0x06, '2': 0x5B, '3': 0x4F, '4': 0x66,
               '5': 0x6D, '6': 0x7D, '7': 0x07, '8': 0x7F, '9': 0x6F,

               ':': 0x09, ';': 0x0d, '<': 0x61, '=': 0x48, '>': 0x43, '?': 0xd3, '@': 0x5f,

               'A': 0x77, 'B': 0x7C, 'C': 0x39, 'D': 0x5E, 'E': 0x79, 'F': 0x71, 'G': 0x3D,
               'H': 0x76, 'I': 0x06, 'J': 0x1E, 'K': 0x76, 'L': 0x38, 'M': 0x55, 'N': 0x54,
               'O': 0x3F, 'P': 0x73, 'Q': 0x67, 'R': 0x50, 'S': 0x6D, 'T': 0x78, 'U': 0x3E,
               'V': 0x1C, 'W': 0x2A, 'X': 0x76, 'Y': 0x6E, 'Z': 0x5B,

               '[': 0x39, '\\': 0x64, ']': 0x0f, '^': 0x23, '_': 0x08, '`': 0x02,
               }

    # 4桁7segment LED表示器のプロファイル
    DISPLAY_PROFILES = {
        "type_0": {         # type_0 : Linear Mapping 4digits and collon
            "digit_mapping": [0, 2, 4, 6],  # 表示桁とRAMアドレスのマッピング
            "colon_address": 8,             # コロン表示用 RAMアドレス
            "digit_count": 5                # 
        },
        "type_1": {         # type_1 : 2 + collon + 2 type
            "digit_mapping": [0, 2, 6, 8],
            "colon_address": 4,
            "digit_count": 5
        }
    }

    @classmethod
    def get_seg(cls, chr: str) -> int:
        ''' segment表示データを取得する '''
        return cls.SEG_MAP.get(chr[0].upper(), 0x00)

    def __init__(self, i2c, address=0x70, type: str='type_0'):
        ''' HT16K33に接続された 4桁7segment LEDディスプレイを操作するクラス '''
        self.i2c = i2c          # I2Cインスタンス
        self.addr = address     # I2Cアドレス

        type = type if type in self.__class__.DISPLAY_PROFILES.keys() else "type_0"
        print(f"{type=}")
        self.PROFILE = self.__class__.DISPLAY_PROFILES[type]
        self.digits = len(self.PROFILE["digit_mapping"])    # 表示桁数
        # self.digit_mappling = self.__class__.DISPLAY_PROFILES["type_1"]["digit_mapping"]

        self._blinkrate = 0

        self._write_cmd(MyHT16K33.OSCILATOR_ON)     # Oscillator ON
        self.clear_display()
        self.set_display(True)                      # Display ON, Blink OFF
        self.set_brightness(15)                     # Brightness = Max

    def _write_cmd(self, data: int):
        ''' コマンドを送信する '''
        self.i2c.writeto(self.addr, bytearray([data & 0xff]))

    def _write_data(self, memaddr: int, buf: bytearray):
        ''' 指定のメモリアドレスにデータを書き込む '''
        self.i2c.writeto_mem(self.addr, memaddr, buf)

    def clear_display(self):
        ''' ディスプレイのデータをクリアする '''
        for i in range(self.PROFILE["digit_count"]):
            self._write_data(i * 2, bytearray([0x00]))

    def set_display(self, on: bool=True):
        ''' ディスプレイを表示／非表示状態にする '''
        if on:
            self._write_cmd(MyHT16K33.DISPLAY_SETUP | 0x01)
        else:
            self._write_cmd(MyHT16K33.DISPLAY_SETUP)

    def set_brightness(self, level: int):
        ''' ディスプレイの明るさを設定する（level = 0 ～ 15:max） '''
        if level:
            self._brightness = max(min(level, 0x0f), 0x00)
            self._write_cmd(self.CMD_BRIGHTNESS | level)
        return self._brightness

    def set_blinkrate(self, rate: int):
        ''' ディスプレイのブリンクレートを設定する（rate = 0:off ～ 3:0.5Hz） '''
        self._blinkrate = max(min(rate, 3), 0)
        self._write_cmd(MyHT16K33.DISPLAY_SETUP | self._blinkrate << 1 | 0x01)

    def write_segment(self, pos: int, data: int):
        ''' ディスプレイの指定桁に表示データを書き込む '''
        adrs = self.PROFILE["digit_mapping"][pos]
        self._write_data(adrs, bytearray([data]))

    def write_data(self, adrs: int, data: int):
        ''' ディスプレイの指定アドレスに表示データを書き込む '''
        # addrs = self.PROFILE["digit_mapping"][adrs] * 2
        self._write_data(adrs, bytearray([data]))

    def set_colon(self):
        self.write_data(self.PROFILE["colon_address"], 0x03)
        # self.write_data(self.digits, 0x03)

    def set_degree(self):
        self.write_data(self.PROFILE["colon_address"], 0x04)

    def set_extra(self, data: int=0x04):
        self.write_data(self.PROFILE["colon_address"], data)

    def write_char(self, pos: int, char: str, dot: bool=False):
        ''' ディスプレイの指定桁に表示文字を書き込む '''
        if 0 <= pos < self.digits:
            char = char[0] if char else ' '
            data = self.__class__.get_seg(char)
            if dot:
                data |= 0x80
            self.write_segment(pos, data)

    def write_number(self, value: float, pos: int=0, width: int=0, precision: int=1 ):
        ''' 浮動小数点数を表示する '''
        data_format = f"{{:{width+1}.{precision}f}}"

        # 浮動小数点数を文字列に変換、文字列を文字のリストに変換する
        # '12.7' -> ['1', '2', '.', '7']
        listval = list(data_format.format(value))
        
        if width:
            listval = listval[:width+1]

        # 小数点を数字に結合する
        # ['1', '2', '.', '7'] -> ['1', '2.', '7']
        sl = []
        for c in listval:
            if c == '.' and sl and sl[-1][-1] != '.':
                sl[-1] += c
            else:
                sl.append(c)

        # 末尾の小数点は消す
        sl[-1] = sl[-1][0]

        # 小数点があれば数字に合成して表示する
        wpos = pos
        for d in sl:
            self.write_char(wpos, d[0], dot=(d[-1] == '.'))
            wpos += 1


    def write_chars(self, chars: str, pos: int=0):
        ''' 文字を表示する '''
        for i, chr in enumerate(chars):
            self.write_segment(i + pos, self.get_seg(chr))



from machine import Pin, I2C
import time




# _SEGMENTS = bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x77\x7C\x39\x5E\x79\x71\x3D\x76\x06\x1E\x76\x38\x55\x54\x3F\x73\x67\x50\x6D\x78\x3E\x1C\x2A\x76\x6E\x5B\x00\x40\x63')

HT16K33_ADDR = 0x70
I2C_SDA = 12
I2C_SCL = 13
I2C_CH = 0

i2c = I2C(I2C_CH, scl=Pin(I2C_SCL, Pin.OUT), sda=Pin(I2C_SDA, Pin.OUT), freq=100000)
addr = i2c.scan()
print(addr)

ht16k = MyHT16K33(i2c, HT16K33_ADDR, type='type_x')
# ht16k.set_display(True)

# ht16k.write_data(4, 0x3)
ht16k.write_char(1, '3', dot=True)

time.sleep(1)

t = -12.5
s = str(t)

# s=['-', '.', '1', '.', '.', '.', '2', '.', '5']
# print(f"{s=}")
sl = []
# sl.append(s[0])

# 小数点の要素を直前の文字（数字）に合体する（単独の小数点はそのまま）
for c in s:
    # if c == '.' and sl and len(sl[-1]) == 1:
    if c == '.' and sl and sl[-1][-1] != '.':
        sl[-1] += c
    else:
        sl.append(c)

ht16k.write_segment(0, 0x1)
time.sleep(1)
ht16k.write_segment(1, 0x2)
time.sleep(1)
ht16k.write_segment(2, 0x4)
time.sleep(1)
ht16k.write_segment(3, 0x8)
time.sleep(1)
ht16k.set_colon()
# ht16k.write_data(2, 0xFD)
# ht16k.write_data(2, 0x2)
print("Done!")
time.sleep(5)
ht16k.clear_display()
ht16k.write_char(3, 'C')
ht16k.write_number(-12.5, width=3)
time.sleep(5)

ht16k.write_number(-2.56, width=3)
time.sleep(5)

ht16k.write_number(2.8666, width=3)
time.sleep(5)

ht16k.write_number(12.72345, width=3)
time.sleep(5)

ht16k.write_number(120.54, width=3)
time.sleep(5)

ht16k.set_colon()
time.sleep(1)
ht16k.set_extra(0x01)
time.sleep(1)
ht16k.set_extra(0x02)
time.sleep(1)
ht16k.set_colon()
time.sleep(1)
ht16k.set_degree()
time.sleep(2)
ht16k.set_extra(0x00)
time.sleep(1)

ht16k.set_colon()
ht16k.write_chars('17')
for i in range(60):
    ht16k.write_chars("{:02}".format(i), 2)
    time.sleep(1)

ht16k.set_blinkrate(2)
time.sleep(3)
ht16k.set_blinkrate(0)
for i in range(16):
    ht16k.set_brightness(i)
    time.sleep(1)


