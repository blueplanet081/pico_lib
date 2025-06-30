# discovery_server.py
import network
import socket
import time
from wifi_config import SSID, PASSWORD

# 各Pico Wの一意なIDを設定 (例: シリアル番号の下位数桁など)
# 複数台Pico Wがある場合、それぞれユニークなIDを設定してください
PICO_ID = "PicoW_A" # ここにこのPico WのIDを設定

# Wi-Fi接続
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# 接続待機
max_wait = 20 # 接続待ち時間を少し長めに設定
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Network connection failed!')
else:
    print('Connected to Wi-Fi.')
    status = wlan.ifconfig()
    print('My IP address:', status[0])

# UDPソケット設定
# サーバーは特定のポートでブロードキャストメッセージを受信待機します
DISCOVERY_PORT = 12345
LISTEN_IP = '0.0.0.0' # すべてのインターフェースからの受信を許可

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((LISTEN_IP, DISCOVERY_PORT))
server_sock.settimeout(0.5) # 受信タイムアウトを設定 (ポーリングのため)

print(f"Discovery server listening on UDP {LISTEN_IP}:{DISCOVERY_PORT}")

try:
    while True:
        try:
            data, addr = server_sock.recvfrom(1024)
            message = data.decode('utf-8').strip()
            
            print(f"Received discovery request from {addr[0]}:{addr[1]}: '{message}'")
            
            # 探索メッセージが "DISCOVER_PICO_W" の場合に応答
            if message == "DISCOVER_PICO_W":
                response_message = f"PICO_W_REPLY:{PICO_ID}:{status[0]}" # IDと自身のIPを返す
                server_sock.sendto(response_message.encode('utf-8'), addr)
                print(f"Sent reply to {addr[0]}:{addr[1]}: '{response_message}'")
        
        except socket.timeout:
            # タイムアウトは何も受信しなかったことを意味するので無視
            pass
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(0.1) # ポーリング間隔
        
except KeyboardInterrupt:
    print("Discovery server stopped.")
finally:
    server_sock.close()
    wlan.active(False)