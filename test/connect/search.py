# discovery_client.py
import network
import socket
import time
from wifi_config import SSID, PASSWORD

# Wi-Fi接続
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# 接続待機
max_wait = 20
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

# ブロードキャストアドレスの決定
# ネットワークアドレスの最後のオクテットを255にする
# 例: IPが 192.168.1.100 なら、ブロードキャストアドレスは 192.168.1.255
ip_parts = status[0].split('.')
BROADCAST_IP = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.255"
DISCOVERY_PORT = 12345
DISCOVERY_MESSAGE = "DISCOVER_PICO_W"

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# ブロードキャストを許可するオプションを設定
client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_sock.settimeout(3) # 応答を待つタイムアウト (秒)

print(f"Sending discovery message to {BROADCAST_IP}:{DISCOVERY_PORT}")

discovered_devices = {}

try:
    # 探索メッセージをブロードキャスト
    client_sock.sendto(DISCOVERY_MESSAGE.encode('utf-8'), (BROADCAST_IP, DISCOVERY_PORT))
    print("Discovery message sent. Waiting for replies...")

    # 応答を収集
    start_time = time.time()
    while time.time() - start_time < client_sock.gettimeout():
        try:
            data, addr = client_sock.recvfrom(1024)
            reply = data.decode('utf-8').strip()
            
            # "PICO_W_REPLY:ID:IP_ADDRESS" 形式の応答を解析
            if reply.startswith("PICO_W_REPLY:"):
                parts = reply.split(':')
                if len(parts) == 3:
                    device_id = parts[1]
                    device_ip = parts[2]
                    
                    if device_id not in discovered_devices:
                        discovered_devices[device_id] = device_ip
                        print(f"Discovered: ID='{device_id}', IP='{device_ip}' from {addr[0]}:{addr[1]}")
                else:
                    print(f"Received malformed reply: {reply} from {addr[0]}:{addr[1]}")
            else:
                print(f"Received unknown reply: {reply} from {addr[0]}:{addr[1]}")
                
        except socket.timeout:
            # タイムアウトしたら応答待ちを終了
            break
        except Exception as e:
            print(f"Error during reception: {e}")
            break # エラーが発生したらループを抜ける

    print("\n--- Discovery complete ---")
    if discovered_devices:
        for device_id, device_ip in discovered_devices.items():
            print(f"  Found device: ID='{device_id}', IP='{device_ip}'")
    else:
        print("No Pico W devices found.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client_sock.close()
    wlan.active(False)