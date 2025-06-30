# async_udp_receiver.py
import network
import socket
import time
import uasyncio as asyncio # uasyncioをインポート
import machine
from wifi_config import SSID, PASSWORD

# Pico Wの内蔵LED
led = machine.Pin("LED", machine.Pin.OUT)

# --- 非同期タスクの定義 ---

async def blink_led(interval_ms):
    """
    指定された間隔でLEDを点滅させる非同期タスク
    """
    while True:
        led.value(1) # LEDオン
        await asyncio.sleep_ms(interval_ms // 2) # 指定間隔の半分待つ
        led.value(0) # LEDオフ
        await asyncio.sleep_ms(interval_ms // 2) # 指定間隔の半分待つ

async def udp_receiver(ip, port):
    """
    UDPデータを受信する非同期タスク
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    # asyncioで使うソケットは非ブロッキングである必要があります
    # settimeout(0) または setblocking(False) を使う
    sock.setblocking(False) 
    
    print(f"UDP receiver listening on {ip}:{port}")

    while True:
        try:
            # await asyncio.wait_for(sock.recvfrom(1024), timeout=1.0) のように直接ソケットを待つことはできません。
            # asyncio.StreamReader などを使うのが一般的ですが、uasyncioでは低レベルのソケット操作の場合、
            # select.poll() を使うか、ソケットがレディになるまでループで待つ必要があります。
            # 簡単化のため、ここでは定期的にrecvfromを試みる形にします。
            # 実際には、uasyncioのstream_reader/writerを使うか、
            # selectモジュールをawaitでラップする方がより効率的です。
            # ここでは簡単なデモとして、すぐに返る非ブロッキングrecvfromをループで回します。
            
            # 注: 本来のasyncioのソケット処理は、データが来るまでCPUを消費せずに待機しますが、
            # MicroPythonの低レベルソケットAPIを直接使う場合、手動でポーリングループを組むとCPUを消費します。
            # 効率的な実装には、uasyncioが提供するより高レベルなネットワークストリームAPI（asyncio.StreamReader/StreamWriter）
            # または asyncio.wait_for() と select.poll() の組み合わせが必要です。
            # しかし、UDPソケットのrecvfromを直接awaitするAPIは、uasyncioには提供されていません。
            # そのため、ここでは非ブロッキングでループを回すか、タイムアウト付きで待ちます。
            # 今回はsocket.settimeout()を使って、データがなければすぐ戻るようにします。
            sock.settimeout(0.1) # 0.1秒待機し、データがなければTimeoutエラー
            
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8').strip()
            print(f"Received from {addr[0]}:{addr[1]}: '{message}'")
            # ここで受信したデータを使った処理を行う
            
        except asyncio.CancelledError:
            # タスクがキャンセルされた場合
            print("UDP receiver task cancelled.")
            break
        except socket.timeout:
            # データがなかった場合、何もしないでループを続行
            # print("No UDP data received (timeout).") # デバッグ用
            pass
        except OSError as e:
            # その他のネットワークエラー
            print(f"UDP socket error: {e}")
            await asyncio.sleep(0.5) # エラー時に少し待機して再試行
        
        await asyncio.sleep_ms(10) # 他のタスクにCPUを譲る

# --- メイン実行部分 ---

async def main():
    """
    メインの非同期関数。Wi-Fi接続とタスクの開始を行う
    """
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
        await asyncio.sleep(1) # 非同期で待機
        
    if wlan.status() != 3:
        raise RuntimeError('Network connection failed!')
    else:
        print('Connected to Wi-Fi.')
        status = wlan.ifconfig()
        my_ip = status[0]
        print('My IP address:', my_ip)

    # 非同期タスクを開始
    # asyncio.create_task() でコルーチンをタスクとしてスケジュールする
    asyncio.create_task(blink_led(500)) # 500ms間隔でLED点滅
    asyncio.create_task(udp_receiver(my_ip, 12345)) # UDP受信を開始

    # ここで他のメインの処理（もしあれば）を非同期で行うか、
    # 単に無限ループでランタイムを維持する
    while True:
        await asyncio.sleep(1) # 1秒ごとに他のタスクに制御を譲る

# uasyncioランタイムを開始
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    # 必要に応じてクリーンアップ
    led.value(0) # LEDオフ
    if wlan.isconnected():
        wlan.active(False)