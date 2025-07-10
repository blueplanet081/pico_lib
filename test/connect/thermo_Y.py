from machine import ADC, Pin
import time
import math


class ValueFilter:
    ''' 時系列の数値を平滑化するフィルタークラス '''
    def __init__(self, filter_type=None, sample_number=0):
        '''
        時系列の数値を平滑化するフィルタークラス

        args:
          filter_type: フィルタータイプ（None, "MED", "MA"）
          　"MED": 中央値
          　"MA": 移動平均
          sample_number: 平滑化のためのサンプル数
        '''
        valid_types = [None, "MA", "MED"]
        if filter_type not in valid_types:
            raise ValueError(f"Filter type must be None, 'MA', or 'MED'.")
            filter_type = None
        self._type = valid_types.index(filter_type)
        print(f"{filter_type=} {self._type=} {sample_number=}")
        self._sample_number = sample_number
        if self._sample_number <= 0:
            if filter_type == "MA":
                self._sample_number = 10    # デフォルトサンプル数（MA）
            elif filter_type == "MED":
                self._sample_number = 7     # デフォルトサンプル数（MED）
        self._buffer = []

    def filterd(self, value):
        ''' フィルターを通した値を返す '''
        if self._type == 0:
            return value

        # サンプル数分バッファに格納する
        self._buffer.append(value)
        if len(self._buffer) > self._sample_number:
            self._buffer.pop(0)

        if self._buffer:
            if self._type == 1:     # MA
                return sum(self._buffer) / len(self._buffer)
            else:                   # MED
                sorted_buffer = sorted(self._buffer)
                return sorted_buffer[len(sorted_buffer) // 2]
        else:
            return(value)


class Thermistor:
    ''' サーミスタで温度測定をするクラス '''
    def __init__(self, pin=26,      # pin番号
                B_constant=3435,    # B定数
                R_ref=10000,        # 基準抵抗値
                R_fixed=None,       # 固定抵抗値
                filter_type=None,   # フィルタータイプ
                sample_number=0     # フィルター用サンプル数
                ) -> None:
        ''' 
        サーミスタを設定する

        args:
          pin: 測定に使用する GPIO番号
          B_constant: サーミスタの B定数
          R_ref: サーミスタの基準抵抗値(ohm)
          R_fixed: 分圧回路の固定抵抗値(ohm)、省略時はサーミスタの基準抵抗値と同じ
          filter_type: フィルタータイプ(None, "MA"（移動平均）, "MED"（中央値）)
          sample_number: フィルター用サンプル数
        '''
        self._pin = pin
        self._adc = ADC(Pin(self._pin))

        self._B_constant = B_constant
        self._R_ref = R_ref

        self._V_supply = 3.3
        self._R_fixed = R_fixed if R_fixed else self._R_ref
        self._T_ref = 25 + 273.15  # 基準温度 25℃ をケルビンに変換

        self._vfilter = ValueFilter(filter_type=filter_type, sample_number=sample_number)

    def get_temperature(self):
        ''' 現在の温度を取得する '''
        adc_raw = self._adc.read_u16()              # ADC測定値
        adc_raw = self._vfilter.filterd(adc_raw)
        V_out = (adc_raw / 65535) * self._V_supply  # センサー電圧

        if self._V_supply - V_out == 0: # ゼロ除算を避ける
            R_T = float('inf')
        else:
            R_T = self._R_fixed * V_out / (self._V_supply - V_out)

        # --- 方法1: B定数を使った簡略版の温度計算 ---
        try:
            temp_K = 1 / (1/self._T_ref + math.log(R_T / self._R_ref) / self._B_constant)
            temp_C = temp_K - 273.15
        except ValueError: # log(負の値) や ゼロ除算の場合
            temp_C = float('nan') # Not a Number

        return temp_C

th1 = Thermistor(26, B_constant=3435, R_fixed=10170, filter_type="MA", sample_number=20)
th11 = Thermistor(28, B_constant=3435, R_fixed=10000, filter_type="MA")
th2 = Thermistor(27, B_constant=3950, R_fixed=100900, R_ref=100000, filter_type="MED")

# メインループ
while True:
    temp_C = th1.get_temperature()
    temp_Cx = th11.get_temperature()
    temp_C2 = th2.get_temperature()
    if not math.isnan(temp_C):
        print(f"Temperature: {temp_C:.2f} C  {temp_Cx:.2f} C  {temp_C2:.2f} C  ({temp_C2 - temp_C:.2f})")
    else:
        print("Error: Could not calculate temperature. Check connections or resistance range.")
    time.sleep(2) # 1秒ごとに読み取り