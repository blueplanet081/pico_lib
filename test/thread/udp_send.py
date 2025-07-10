'''
_threadを使って、UDPでデータを送信する例
'''

import network
import socket
import time
import struct

# 設定
SSID = 'your_wifi_ssid'
PASSWORD = 'your_wifi_password'
DEST_IP = '192.168.1.255'   # ブロードキャストも可能（受信側が許容していれば）
DEST_PORT = 12345
SENDER_ID = 42  # 各送信元で異なるIDを設定

def wifi_setup():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
    print("Connected:", wlan.ifconfig())

def send_packet(seq, timestamp, message):
    msg = message.encode()[:20]  # 最大20バイトまで
    msg += b'\x00' * (20 - len(msg))  # パディング
    packet = struct.pack('<III20s', SENDER_ID, seq, timestamp, msg)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(packet, (DEST_IP, DEST_PORT))
    sock.close()
    print(f"Sent: ID={SENDER_ID}, Seq={seq}, Time={timestamp}, Msg={message}")

wifi_setup()

sequence = 0
while True:
    now = int(time.time())
    send_packet(sequence, now, "Hello from sender")
    sequence += 1
    time.sleep(3)