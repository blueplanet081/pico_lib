# thread_udp_receiver.py
import network
import socket
import time
import machine
import _thread # _threadモジュールをインポート
from wifi_config import SSID, PASSWORD

# Pico Wの内蔵LED
led = machine.Pin("LED", machine.Pin.OUT)

# --- グローバル変数とロック（簡略化）---
# スレッド間でデータを共有するためのグローバル変数
# 受信したデータがあればここに格納される
global_received_data = None
global_received_addr = None

# ロックは、グローバル変数へのアクセスを同期するために使用されます。
# 単純なフラグやデータ更新の場合は必ずしも必須ではありませんが、
# 複雑なデータ構造を共有する場合は必須です。
# lock = _thread.allocate_lock() # 今回はシンプル化のため使用しませんが、通常は検討すべき

# --- スレッド関数 ---

def udp_receiver_thread(ip, port):
    """
    バックグラウンドでUDPデータを受信するスレッド関数
    このスレッドはデータが来るまでブロッキングモードで待機します
    """
    global global_received_data
    global global_received_addr

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    # ここはブロッキングモードのまま (デフォルト)

    print(f"[UDP Thread] Listening on {ip}:{port} (Blocking mode)")

    try:
        while True:
            # データが来るまでここで完全にブロックされますが、
            # メインスレッドはブロックされません
            data, addr = sock.recvfrom(1024) 
            message = data.decode('utf-8').strip()
            
            # lock.acquire() # データ更新前にロックを取得 (推奨されるが、ここでは簡略化)
            global_received_data = message
            global_received_addr = addr
            # lock.release() # データ更新後にロックを解放 (推奨されるが、ここでは簡略化)

            print(f"[UDP Thread] Received: '{message}' from {addr[0]}:{addr[1]}")
            
    except Exception as e:
        print(f"[UDP Thread] Error: {e}")
    finally:
        sock.close()
        print("[UDP Thread] Socket closed.")

# --- メインプログラム ---

def main():
    # Wi-Fi接続
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print('Connecting to Wi-Fi...')
    max_wait = 20
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        time.sleep(1) # ここはメインスレッドでブロッキングされる

    if wlan.status() != 3:
        raise RuntimeError('Network connection failed!')
    else:
        print('Connected to Wi-Fi.')
        status = wlan.ifconfig()
        my_ip = status[0]
        print('My IP address:', my_ip)

    # UDP受信スレッドを開始
    # 第2引数はタプルで、スレッド関数に渡す引数を指定します
    _thread.start_new_thread(udp_receiver_thread, (my_ip, 12345))

    print("[Main Thread] LED blinking and checking for received data...")
    blink_interval_ms = 500
    last_blink_time = time.ticks_ms()

    try:
        while True:
            current_time = time.ticks_ms()
            if time.ticks_diff(current_time, last_blink_time) >= blink_interval_ms:
                led.value(not led.value()) # LEDの状態を反転
                last_blink_time = current_time

            # グローバル変数にデータがあれば表示し、リセット
            if global_received_data is not None:
                # lock.acquire() # データ読み取り前にロックを取得 (推奨されるが、ここでは簡略化)
                print(f"[Main Thread] Processing received data: {global_received_data} from {global_received_addr[0]}")
                # データを処理したら、Noneに戻して次の受信を待つ
                global_received_data = None
                global_received_addr = None
                # lock.release() # データ読み取り後にロックを解放 (推奨されるが、ここでは簡略化)

            time.sleep_ms(10) # メインスレッドのCPU消費を抑えるため少しスリープ

    except KeyboardInterrupt:
        print("[Main Thread] Program stopped by user.")
    finally:
        # スレッドの終了処理はMicroPythonでは難しい場合が多いです。
        # 通常、プログラム終了時に自動的にクリーンアップされます。
        led.value(0) # LEDオフ
        if wlan.isconnected():
            wlan.active(False)

# メイン関数を実行
if __name__ == '__main__':
    main()