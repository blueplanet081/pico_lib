import gc
import time
import network
import sys

def help():
    print("show_memory_info() : Display memory usage")
    print("run(filename) : Execute a program on Pico")
    print("delete_module(modulename='neos') : Remove imported module")
    print("wlan_connect() : Connect to a specified wireless network")
    print("wlan_isconnected() : Check if connected to a wireless network")
    print("wlan_disconnect() : Disconnect from a wireless network")
    print("wlan_scan(): Scan for available wireless networks")
    print("wlan_ifconfig() : Get IP address, subnet mask, gateway, and DNS server")
    print("wlan_config(param=None) : Get network interface parameters")

def show_memory_info():
    ''' メモリの使用状況を表示 '''
    gc.collect()
    use = gc.mem_alloc()
    remain = gc.mem_free()
    total = use + remain
    print("memory info:")
    print(f"  total:  {total:8,} bytes")
    print(f"  use:    {use:8,} bytes  ({use/total*100:.2}%)")
    print(f"  remain: {remain:8,} bytes")


def run(filename):
    ''' pico上のプログラムを実行 '''
    global_vars = globals().copy()
    global_vars['__name__'] = '__main__'
    exec(open(filename).read(), global_vars)


def show_name():
    print(f"{__name__=}")

def show_locals():
    print(f"{locals()=}")

def delete_module(modulename='neos'):
    ''' importしたモジュールを削除する '''
    print(f"try to delete {modulename=}")
    del sys.modules[modulename]

def wlan_connect():
    ''' 指定のワイヤレスネットワークに接続する '''
    ssid = const("YOUR_SSID")           # 接続するWi-FiのSSID
    passwd = const("YOUR_PASSWORD")     # 接続するWi-Fiのパスワード

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(f"try to connect {ssid=} {passwd=}")
    wlan.connect(ssid, passwd)

    # 接続完了まで待機
    while not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        time.sleep(1)

    print('Connected to Wi-Fi')
    print('IP address:', wlan.ifconfig()[0])

def wlan_isconnected():
    ''' ワイヤレスネットワークに接続されているかどうか '''
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(f"{wlan.isconnected()=}")

def wlan_disconnect():
    ''' ワイヤレスネットワークから切断する '''
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # if wlan:
    wlan.disconnect()

def wlan_scan():
    ''' 利用可能なワイヤレスネットワークをスキャンする '''
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    for info in wlan.scan():
        print(info)

def wlan_ifconfig():
    ''' IPアドレス、サブネットマスク、ゲートウェイ、DNSサーバーを取得する '''
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('IP address:', wlan.ifconfig()[0])
    print(wlan.ifconfig())

def wlan_config(param=None):
    ''' ネットワークインターフェースパラメータを取得する '''
    if param is None:
        print("You must specify 'mac', 'ssid', 'channel', 'security', 'hostname'  or 'txpower' as a parameter.")
        return
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ret = wlan.config(param)
    if type(ret) is int:
        print(f"wlan.config('{param}')={ret}({hex(ret)})")
    elif type(ret) is bytes:
        print(f"wlan.config('{param}')={ret}(0x{ret.hex()})")
    else:
        print(f"wlan.config('{param}')={ret}")
