import gc
import time
import network
import sys
import os
import machine

def getkeys_from_kv_tuple(data):
    ''' key=value形式の特殊なtupleから、keyのリストを取得する '''
    w_keys = str(data)[1:-1].split("=")[0:-1]
    return [key[key.rfind(' ') + 1:] for key in w_keys]

def makedict_from_kv_tuple(data):
    ''' key=value形式の特殊なtupleを辞書形式に変換する '''
    keys = getkeys_from_kv_tuple(data)
    return {key: value for key, value in zip(keys, data)}

def help():
    print("show_memory_info() : Display memory usage.")
    print("show_frequency() : Display the operating frequency.")
    print("show_version() : Display the MicroPython interpreter version.")
    print("show_implementation() : Display MicroPython implementation details.")
    print("show_uname() : Display basic system and device information.")
    print("show_unique_id() : Display the unique ID of the machine.")
    print("run(filename) : Execute a program on the Pico.")
    print("delete_module(modulename='neos') : Remove an imported module.")
    print()
    print("wlan_connect() : Connect to a specified wireless network.")
    print("wlan_isconnected() : Check if connected to a wireless network.")
    print("wlan_disconnect() : Disconnect from a wireless network.")
    print("wlan_scan(): Scan for available wireless networks.")
    print("wlan_ifconfig() : Retrieve IP address, subnet mask, gateway, and DNS server.")
    print("wlan_config(param=None) : Retrieve network interface parameters.")

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

def show_frequency():
    ''' 動作周波数を表示 '''

    print(f"{machine.freq()=} ({machine.freq():,}Hz)")


def show_version():
    ''' MicroPythonのバージョン情報を表示 '''
    print(f"{sys.version=}")

def show_implementation():
    ''' MicroPythonの実装情報を表示 '''
    print(f"{sys.implementation=}")
    print()

    dict_info = makedict_from_kv_tuple(sys.implementation)
    for key in getkeys_from_kv_tuple(sys.implementation):
        value = dict_info[key]
        if type(value) is str:
            print(f"{key}: '{value}'")
        else:
            print(f"{key}: {value}")

def show_uname():
    ''' システムやデバイスの基本情報を表示 '''
    uname = os.uname()
    print(f"os.uname()={uname}")
    print()

    dict_uname = makedict_from_kv_tuple(uname)
    for key in getkeys_from_kv_tuple(uname):
        print(f"{key}: '{dict_uname[key]}'")

def show_unique_id():
    ''' 固有IDを表示 '''
    id = machine.unique_id()
    print(f"machine.unique_id()={id}(0x{id.hex()})")

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
    import wlan_info as info
    ssid = info.ssid
    passwd = info.passwd

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(f"try to connect {ssid=} {passwd=}")
    wlan.connect(ssid, passwd)

    count = 0
    while not wlan.isconnected():
        if count >= 10:
            print("Can't connect to Wi-Fi")
            return
        count += 1
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
