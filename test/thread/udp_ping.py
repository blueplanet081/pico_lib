'''
受信側（スキャナ）、複数IPに PING
'''

import network
import socket
import time

SSID = 'your_wifi_ssid'
PASSWORD = 'your_wifi_password'
PORT = 54321  # 相手の応答ポート
SCAN_IPS = ['192.168.1.101', '192.168.1.102', '192.168.1.103']  # スキャン対象

def wifi_setup():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass

wifi_setup()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.5)

for ip in SCAN_IPS:
    try:
        sock.sendto(b'PING', (ip, PORT))
        data, addr = sock.recvfrom(128)
        if data == b'PONG':
            print(f"{ip} is online")
    except:
        print(f"{ip} is unreachable")

sock.close()