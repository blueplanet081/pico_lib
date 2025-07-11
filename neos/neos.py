import gc
import time
import network
import sys
import os
import machine
import ntptime

# リセットコード
RESET = "\x1b[0m"

# 文字色
RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE = "\x1b[34m"
MAGENTA = "\x1b[35m"
CYAN = "\x1b[36m"
WHITE = "\x1b[37m"

# 太字
BOLD = "\x1b[1m"

# 背景色
BG_RED = "\x1b[41m"
BG_GREEN = "\x1b[42m"

def getkeys_from_kv_tuple(data):
    ''' key=value形式の特殊なtupleから、keyのリストを取得する '''
    w_keys = str(data)[1:-1].split("=")[0:-1]
    return [key[key.rfind(' ') + 1:] for key in w_keys]

def makedict_from_kv_tuple(data):
    ''' key=value形式の特殊なtupleを辞書形式に変換する '''
    keys = getkeys_from_kv_tuple(data)
    return {key: value for key, value in zip(keys, data)}

def get_localtime(etime: int | None = None, tzone: int = 9):
    ''' ローカルタイムを取得する '''
    if etime is None:
        etime = time.time()
    return time.gmtime(etime + tzone * 3600)

def str_ftime(timestamp_seconds):
    t = get_localtime(timestamp_seconds, tzone=9)
    # 年/月/日 時:分:秒 の形式でフォーマット
    return f"{t[0]:04d}/{t[1]:02d}/{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}"

def info():
    show_help()

def show_help():
    print(YELLOW + "show_help() or info()" + RESET + " : Display this message.")
    print(YELLOW + "show_memory_info()" + RESET + " : Display memory usage.")
    print(YELLOW + "show_frequency()" + RESET + " : Display the operating frequency.")
    print(YELLOW + "show_version()" + RESET + " : Display the MicroPython interpreter version.")
    print(YELLOW + "show_implementation()" + RESET + " : Display MicroPython implementation details.")
    print(YELLOW + "show_uname()" + RESET + " : Display basic system and device information.")
    print(YELLOW + "show_unique_id()" + RESET + " : Display the unique ID of the machine.")
    print(YELLOW + "show_files()" + RESET + " : List Files and Directories")
    print(YELLOW + "run('filename')" + RESET + " : Execute a program on the Pico.")
    print(YELLOW + "delete_module(modulename='neos')" + RESET + " : Remove an imported module.")
    print()
    print(YELLOW + "wlan_connect()" + RESET + " : Connect to a specified wireless network.")
    print(YELLOW + "wlan_isconnected()" + RESET + " : Check if connected to a wireless network.")
    print(YELLOW + "wlan_disconnect()" + RESET + " : Disconnect from a wireless network.")
    print(YELLOW + "wlan_scan()" + RESET + ": Scan for available wireless networks.")
    print(YELLOW + "wlan_ifconfig()" + RESET + " : Retrieve IP address, subnet mask, gateway, and DNS server.")
    print(YELLOW + "wlan_config(param=None)" + RESET + " : Retrieve network interface parameters.")
    print(YELLOW + "set_ntp()" + RESET + " : Set Time from an NTP Server.")
    print(YELLOW + "show_localtime()" + RESET + " : Display Current Time (UTC+9).")
    print(YELLOW + "show_gmtime()" + RESET + " : Display Current Time (UTC).")

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

def set_ntp():
    ''' NTPサーバから時刻を取得して設定する '''
    wlan_connect()
    ntptime.settime()

    for _ in range(5):
        t = get_localtime()
        print(f"{t[0]:04d}/{t[1]:02d}/{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}")
        time.sleep(0.5)

def show_localtime():
    ''' 現在時刻を表示する（UTC+9）'''    
    t = get_localtime()
    print(f"{t[0]:04d}/{t[1]:02d}/{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}")

def show_gmtime():
    ''' 現在時刻を表示する（UTC）'''    
    t = get_localtime(tzone=0)
    print(f"{t[0]:04d}/{t[1]:02d}/{t[2]:02d} {t[3]:02d}:{t[4]:02d}:{t[5]:02d}")

def show_files():
    ''' ファイルとディレクトリの一覧を表示する '''
    def show_files(path='/', indent=0):
        """
        指定されたパス以下のファイルとディレクトリを再帰的にリスト表示します。
        ファイル名、サイズ、最終更新日時を表示します。
        """
        try:
            contents = os.listdir(path)
            
            # ディレクトリ一覧
            directories = sorted([c for c in contents if (os.stat(f"{path}/{c}")[0] & 0o170000) == 0o040000])
            # ファイル一覧
            files = sorted([c for c in contents if (os.stat(f"{path}/{c}")[0] & 0o170000) == 0o100000])

            current_indent = "  " * indent

            for item in directories:
                full_path = f"{path}/{item}"
                print(f"{current_indent}{item}/")
                show_files(full_path, indent + 1)
            
            for item in files:
                full_path = f"{path}/{item}"
                try:
                    stats = os.stat(full_path)
                    file_size = stats[6]
                    m_time = str_ftime(stats[8])     # last modified timeのつもり
                

                    print(f"{current_indent}{item:<16} {file_size:>10,} bytes  {m_time}")
                except OSError as e:
                    print(f"{current_indent}{item:<16} Error getting info: {e}")

        except OSError as e:
            print(f"Error accessing path '{path}': {e}")


    # ルートディレクトリから探索を開始
    show_files()

print(GREEN + BOLD, end="")
print('"neos" is a MicroPython module for displaying information about '
      'the Raspberry Pi Pico / Pico W and performing simple operations within the vREPL environment.')
print(RESET, end="")
print('Type "show_help()" or "info()" for more information.')