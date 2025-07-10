# 移動平均フィルタのための設定
window_size_ma = 10 # 移動平均を計算するサンプル数

# 測定値を保存するためのリスト
measurement_buffer_ma = []

def get_filtered_adc_ma():
    global measurement_buffer_ma

    # 新しいADC値を読み取り、バッファに追加
    new_adc_value = read_raw_adc()
    measurement_buffer_ma.append(new_adc_value)

    # バッファが指定サイズを超えたら、最も古い値を除去
    if len(measurement_buffer_ma) > window_size_ma:
        measurement_buffer_ma.pop(0) # リストの先頭要素を削除

    # バッファ内の値の平均を計算
    if measurement_buffer_ma:
        return sum(measurement_buffer_ma) / len(measurement_buffer_ma)
    else:
        return 0 # バッファが空の場合は0を返すか、エラー処理

# メインループでの使用例
print("--- 移動平均フィルタのデモ ---")
for i in range(20): # 20回分の測定をシミュレート
    filtered_adc_value = get_filtered_adc_ma()
    raw_adc_value = read_raw_adc() # フィルタリング前の生の値も表示
    print(f"Iteration {i+1}: Raw ADC = {raw_adc_value}, Filtered (MA) ADC = {filtered_adc_value:.2f}")
    time.sleep(0.1) # 実際はサーミスタの読み取り間隔に合わせる