import time

def constant_interval_loop(interval):
    """
    一定間隔で処理を繰り返す関数。

    Args:
        interval (int or float): 処理の繰り返し間隔（秒）。
    """
    next_time = time.time() + interval

    while True:
        # ここに実行したい処理を書く
        # 例: print()
        print(f"現在の時刻: {time.time()}")
        
        # 処理が長くなる可能性がある場合、sleep()の時間を調整するために、
        # 処理の最後に現在時刻を再度取得する
        processing_start_time = time.time()
        
        # ここに時間のかかる処理を追加してみる
        time.sleep(0.5) 
        
        processing_end_time = time.time()
        
        # 次のループ開始時刻まで待機する
        next_time += interval
        sleep_duration = next_time - time.time()
        
        # 待機時間が負になる場合は、すでに次の間隔を超えているため、
        # sleep()せずにすぐに次のループへ進む
        if sleep_duration > 0:
            time.sleep(sleep_duration)

if __name__ == "__main__":
    # 5秒間隔でループを実行
    interval = 5
    constant_interval_loop(interval)