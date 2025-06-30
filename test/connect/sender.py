# sender.py
import network
import socket
import time
import random # 温度シミュレーション用
# from wifi_config import SSID, PASSWORD
from wlan_info import ssid, passwd


# 受信側のPico WのIPアドレスに置き換えてください！
# 受信側を起動し、そのPico WのIPアドレスを確認してからここに設定してください。
RECEIVER_IP = "192.168.0.38"
RECEIVER_PORT = 12345 # 受信側と合わせる

# Wi-Fi接続
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, passwd)

# 接続待機
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('My IP address:', status[0])

# UDPソケット作成
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Sending data to {RECEIVER_IP}:{RECEIVER_PORT}")

try:
    while True:
        # 温度センサーの値のシミュレーション (例: 20.0〜30.0の範囲)
        temperature = 20.0 + (random.random() * 10.0)
        
        # floatを文字列に変換して送信
        message = f"{temperature:.2f}"
        
        sock.sendto(message.encode('utf-8'), (RECEIVER_IP, RECEIVER_PORT))
        print(f"Sent: {message}")
        
        time.sleep(2) # 2秒ごとに送信
except KeyboardInterrupt:
    print("Sender stopped.")
finally:
    sock.close()
    wlan.active(False)