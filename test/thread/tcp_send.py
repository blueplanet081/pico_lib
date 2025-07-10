'''
_threadを使って、TCPでデータを送信する例
'''

import network
import socket
import time
import struct

SSID = 'your_wifi_ssid'
PASSWORD = 'your_wifi_password'
DEST_IP = '192.168.1.100'  # 受信側のIP
DEST_PORT = 12345

def wifi_setup():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
    print("Connected:", wlan.ifconfig())

def send_structured_data(seq, timestamp, message):
    try:
        msg = message.encode()[:20]  # 最大20バイトに制限
        msg += b'\x00' * (20 - len(msg))  # パディング
        packet = struct.pack('<II20s', seq, timestamp, msg)

        addr = socket.getaddrinfo(DEST_IP, DEST_PORT)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(packet)
        s.close()
        print(f"Sent: seq={seq}, time={timestamp}, msg={message}")
    except Exception as e:
        print("Send failed:", e)

wifi_setup()

sequence = 0
while True:
    now = int(time.time())
    test_message = "Hello Pico!"
    send_structured_data(sequence, now, test_message)
    sequence += 1
    time.sleep(5)