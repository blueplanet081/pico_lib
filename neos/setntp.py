from micropython import const
import network
import ntptime
import time
from machine import Pin, I2C


def get_localtime(etime: int | None = None, tzone: int = 9):
    ''' ローカルタイムを取得する '''
    if etime is None:
        etime = time.time()
    return time.gmtime(etime + tzone * 3600)


ssid = const("BCW710J-BDC0A-G")
passwd = const("ce55848c534ac")

def connect_wifi(ssid, passed):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, passwd)

    # 接続完了まで待機
    while not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        time.sleep(1)

    print('Connected to Wi-Fi')
    print('IP address:', wlan.ifconfig()[0])

# set_ntp(wifi)
connect_wifi(ssid, passwd)
ntptime.settime()


for _ in range(5):
    t = get_localtime()
    print(f"{t[0]:04d}/{t[1]:02d}/{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}")
    time.sleep(0.5)
