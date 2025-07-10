'''
_threadを使って、UDPでデータを受信する例
'''

import network
import socket
import time
import struct
import _thread

SSID = 'your_wifi_ssid'
PASSWORD = 'your_wifi_password'
PORT = 12345
PACKET_SIZE = 28  # structサイズ = 4 + 4 + 4 + 20

shared_data = []
data_lock = _thread.allocate_lock()

def wifi_setup():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.5)
    print("Connected:", wlan.ifconfig())

def listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', PORT))
    print("Listening on UDP port", PORT)

    while True:
        try:
            packet, addr = sock.recvfrom(PACKET_SIZE)
            if len(packet) == PACKET_SIZE:
                sender_id, seq, ts, raw = struct.unpack('<III20s', packet)
                msg = raw.decode().rstrip('\x00')
                with data_lock:
                    shared_data.append({
                        'sender': sender_id,
                        'sequence': seq,
                        'timestamp': ts,
                        'message': msg,
                        'ip': addr[0]
                    })
        except Exception as e:
            print("Receive error:", e)

def get_next():
    with data_lock:
        if shared_data:
            return shared_data.pop(0)
        else:
            return None

wifi_setup()
_thread.start_new_thread(listener, ())

while True:
    entry = get_next()
    if entry:
        print(f"From {entry['sender']} @ {entry['ip']}: [{entry['sequence']}] {entry['message']} (time={entry['timestamp']})")
    time.sleep(0.2)