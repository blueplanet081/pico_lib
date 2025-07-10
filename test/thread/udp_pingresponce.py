'''
応答ノード、PINGに反応
'''

import network
import socket

SSID = 'your_wifi_ssid'
PASSWORD = 'your_wifi_password'
PORT = 54321  # 応答を受け取るポート

def wifi_setup():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass

wifi_setup()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', PORT))
print("Responder ready.")

while True:
    data, addr = s.recvfrom(128)
    if data == b'PING':
        s.sendto(b'PONG', addr)