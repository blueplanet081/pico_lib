# 中央値フィルタのための設定
window_size_median = 7 # 中央値を計算するサンプル数 (奇数にすると中央値が明確)

# 測定値を保存するためのリスト
measurement_buffer_median = []

def get_filtered_adc_median():
    global measurement_buffer_median

    # 新しいADC値を読み取り、バッファに追加
    new_adc_value = read_raw_adc()
    measurement_buffer_median.append(new_adc_value)

    # バッファが指定サイズを超えたら、最も古い値を除去
    if len(measurement_buffer_median) > window_size_median:
        measurement_buffer_median.pop(0)

    # バッファ内の値をソートし、中央値を取得
    if measurement_buffer_median:
        sorted_buffer = sorted(measurement_buffer_median)
        # 中央のインデックスを計算
        median_index = len(sorted_buffer) // 2
        return sorted_buffer[median_index]
    else:
        return 0 # バッファが空の場合は0を返すか、エラー処理

# メインループでの使用例
print("\n--- 中央値フィルタのデモ ---")
for i in range(20): # 20回分の測定をシミュレート
    filtered_adc_value = get_filtered_adc_median()
    raw_adc_value = read_raw_adc() # フィルタリング前の生の値も表示
    print(f"Iteration {i+1}: Raw ADC = {raw_adc_value}, Filtered (Median) ADC = {filtered_adc_value}")
    time.sleep(0.1)