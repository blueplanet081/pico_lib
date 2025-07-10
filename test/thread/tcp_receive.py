'''
_threadを使って、TCPでデータを受信する例
'''

import network
import socket
import _thread
import time
import struct

shared_list = []
list_lock = _thread.allocate_lock()

SSID = 'your_wifi_ssid'
PASSWORD = 'your_wifi_password'
PORT = 12345

def wifi_setup():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
    print("Connected:", wlan.ifconfig())

def listener_thread():
    addr = socket.getaddrinfo('0.0.0.0', PORT)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Listening...")

    while True:
        conn, _ = s.accept()
        packet = conn.recv(28)  # struct サイズ = 4 + 4 + 20 = 28 bytes
        conn.close()

        if packet and len(packet) == 28:
            seq, ts, raw_msg = struct.unpack('<II20s', packet)
            msg = raw_msg.decode().rstrip('\x00')
            with list_lock:
                shared_list.append((seq, ts, msg))

def get_next_data():
    with list_lock:
        if shared_list:
            return shared_list.pop(0)
        return None

wifi_setup()
_thread.start_new_thread(listener_thread, ())

while True:
    item = get_next_data()
    if item:
        seq, ts, msg = item
        print(f"Received: seq={seq}, time={ts}, msg={msg}")
    time.sleep(0.2)