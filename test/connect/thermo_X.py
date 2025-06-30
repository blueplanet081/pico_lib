from machine import ADC, Pin
import time
import math

# ADCピンの定義 (GP28を例とします)
adc_pin = 26
thermistor_adc = ADC(Pin(adc_pin))

# 電圧分圧回路の定数
# Raspberry Pi Pico WのVccは3.3V
V_supply = 3.3
# 直列に接続する固定抵抗の値 (10kΩ)
R_fixed = 10000

# サーミスタのB定数 (MF52D 10K B3435 1% から)
B_constant = 3950

# --- 方法1: B定数を使った簡略版の温度計算 (近似) ---
# NTCサーミスタの抵抗値と温度の関係式 (近似)
# R_T = R_0 * exp(B * (1/T - 1/T_0))
# ここで、R_Tは温度Tにおける抵抗値、R_0は基準温度T_0における抵抗値（25℃で10kΩ）、BはB定数。
# TとT_0はケルビン温度。
R_ref = 10000  # 25℃における抵抗値 (10K)
T_ref = 25 + 273.15  # 基準温度 25℃ をケルビンに変換

# ADCから電圧を読み取り、温度を計算する関数
def read_temperature():
    # ADCから生の値 (0-65535) を読み取る
    adc_raw = thermistor_adc.read_u16()

    # 生の値を電圧 (0-3.3V) に変換
    # Raspberry Pi Pico WのADCは16ビット分解能 (0-65535)
    V_out = (adc_raw / 65535) * V_supply

    # 電圧分圧の式からサーミスタの抵抗値 R_T を計算
    # V_out = V_supply * (R_T / (R_fixed + R_T))
    # R_T = R_fixed * V_out / (V_supply - V_out)
    if V_supply - V_out == 0: # ゼロ除算を避ける
        R_T = float('inf')
    else:
        R_T = R_fixed * V_out / (V_supply - V_out)

    # --- 方法1: B定数を使った簡略版の温度計算 ---
    try:
        # temp_K_b_const = 1 / (1/T_ref + (1/B_constant) * math.log(R_T / R_ref))
        temp_K_b_const = 1 / (1/T_ref + math.log(R_T / R_ref) / B_constant)
        temp_C_b_const = temp_K_b_const - 273.15
    except ValueError: # log(負の値) や ゼロ除算の場合
        temp_C_b_const = float('nan') # Not a Number

    return temp_C_b_const, R_T


# メインループ
while True:
    temperature_celsius, resistance = read_temperature()
    if not math.isnan(temperature_celsius):
        print(f"Resistance: {resistance:.2f} Ohms, Temperature: {temperature_celsius:.2f} C")
    else:
        print("Error: Could not calculate temperature. Check connections or resistance range.")
    time.sleep(1) # 1秒ごとに読み取り