# receiver.py
import network
import socket
import time
# from wifi_config import SSID, PASSWORD
from wlan_info import ssid, passwd

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
    print('IP address:', status[0])

# UDPソケット設定
# 受信ポート番号は送信側と合わせる必要があります
UDP_IP = status[0]  # 自身のIPアドレスでListen
UDP_PORT = 12345    # 送信側と合わせる

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on UDP {UDP_IP}:{UDP_PORT}")

try:
    while True:
        data, addr = sock.recvfrom(1024) # バッファサイズは適宜調整
        # 受信したデータをfloatにデコード
        # floatのバイナリ表現を直接送受信する場合、structモジュールを使うと確実です。
        # 簡単のために、ここでは文字列として送信し、floatに変換します。
        try:
            received_float = float(data.decode('utf-8').strip())
            print(f"Received from {addr[0]}:{addr[1]}: {received_float:.2f}")
        except ValueError:
            print(f"Received non-float data from {addr[0]}:{addr[1]}: {data.decode('utf-8').strip()}")
except KeyboardInterrupt:
    print("Receiver stopped.")
finally:
    sock.close()
    wlan.active(False)