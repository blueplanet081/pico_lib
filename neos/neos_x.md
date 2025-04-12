
# neos モジュール <!-- omit in toc -->

## 目的 <!-- omit in toc -->

- Raspberry Pi pico / pico W の情報を MicroPythonの REPL環境に表示したり、簡単な操作を指定するためのモジュールです。
  
## 動作環境、テスト環境 <!-- omit in toc -->

- Raspberry Pi pico（ネットワーク関連の機能を除く）、pico W を接続した MicroPythonの REPL環境で動作します。
- 以下の環境で動作確認をしています。
  - Visual Studio Code/MicroPico の REPL環境
  - Raspberry Pi pico W
  - sys.version=3.4.0; MicroPython v1.23.0 on 2024-06-02

## ファイル一覧 <!-- omit in toc -->

- neos.py（モジュール本体）
- wlan_info.py（Wi-Fiに接続する情報を格納した設定ファイル）

## インストール <!-- omit in toc -->

- Raspberry Pi pico / pico W のルート、または libディレクトリへ以下のファイルを配置する
  - neos.py
  - wlan_info.py（wlan_connectを使用する場合に必要）

<br>
<br>

# 関数一覧 <!-- omit in toc -->

- [1. 　help()　関数一覧を表示する](#1-help関数一覧を表示する)
- [2. 　show\_memory\_info()　メモリの使用状況を表示する](#2-show_memory_infoメモリの使用状況を表示する)
- [3. 　show\_version()　MicroPythonのバージョン情報を表示する](#3-show_versionmicropythonのバージョン情報を表示する)
- [4. 　show\_implementation()　MicroPythonの実装情報を表示する](#4-show_implementationmicropythonの実装情報を表示する)
- [5. 　show\_unique\_id()　固有IDを表示する](#5-show_unique_id固有idを表示する)
- [6. 　run()　pico上のプログラムを実行する](#6-runpico上のプログラムを実行する)
- [7. 　delete\_module()　importしたモジュールを削除する](#7-delete_moduleimportしたモジュールを削除する)
- [8. 　wlan\_connect()　指定のワイヤレスネットワークに接続する](#8-wlan_connect指定のワイヤレスネットワークに接続する)
- [9. 　wlan\_isconnected()　ワイヤレスネットワークに接続されているかどうかを判断する](#9-wlan_isconnectedワイヤレスネットワークに接続されているかどうかを判断する)
- [10. 　wlan\_disconnect()　ワイヤレスネットワークから切断する](#10-wlan_disconnectワイヤレスネットワークから切断する)
- [11. 　wlan\_scan()　利用可能なワイヤレスネットワークをスキャンする](#11-wlan_scan利用可能なワイヤレスネットワークをスキャンする)
- [12. 　wlan\_ifconfig()　IPアドレス、サブネットマスク、ゲートウェイ、DNSサーバーを取得する](#12-wlan_ifconfigipアドレスサブネットマスクゲートウェイdnsサーバーを取得する)
- [13. 　wlan\_config()　ネットワークインターフェースパラメータを取得する](#13-wlan_configネットワークインターフェースパラメータを取得する)

## 1. 　help()　関数一覧を表示する

- neosモジュールで使える関数の一覧を表示する

### 実行例 <!-- omit in toc -->

```python
MicroPython v1.23.0 on 2024-06-02; Raspberry Pi Pico W with RP2040
Type "help()" for more information or .help for custom vREPL commands.

>>> import neos
>>> neos.help()
show_memory_info() : Display memory usage
show_version() : Display MicroPython interpreter version
show_implementation() : Display MicroPython implementation
show_unique_id() : Display unique id of machine
run(filename) : Execute a program on Pico
delete_module(modulename='neos') : Remove imported module

wlan_connect() : Connect to a specified wireless network
wlan_isconnected() : Check if connected to a wireless network
wlan_disconnect() : Disconnect from a wireless network
wlan_scan(): Scan for available wireless networks
wlan_ifconfig() : Get IP address, subnet mask, gateway, and DNS server
wlan_config(param=None) : Get network interface parameters
>>> 
```

## 2. 　show_memory_info()　メモリの使用状況を表示する

- 現在のメモリの使用状況を表示する

### 実行例 <!-- omit in toc -->

```python
>>> neos.show_memory_info()
memory info:
  total:   191,424 bytes
  use:       8,400 bytes  (4.4%)
  remain:  183,024 bytes
>>> 
```

## 3. 　show_version()　MicroPythonのバージョン情報を表示する

- 現在動作している MicroPythonのバージョン情報を表示する

### 実行例 <!-- omit in toc -->

```python
>>> neos.show_version()
sys.version=3.4.0; MicroPython v1.23.0 on 2024-06-02
>>> 
```

## 4. 　show_implementation()　MicroPythonの実装情報を表示する

- 現在動作している MicrPythonの実装情報を表示する

### 実行例 <!-- omit in toc -->

```python
>>> neos.show_implementation()
sys.implementation=(name='micropython', version=(1, 23, 0, ''), _machine='Raspberry Pi Pico W with RP2040', _mpy=4870)
>>> 
```

## 5. 　show_unique_id()　固有IDを表示する

- マシンの固有IDを表示する
- 固有IDは byte型オブジェクトで、（）内はそれを 16進数表示したもの

### 実行例 <!-- omit in toc -->

```python
>>> neos.show_unique_id()
machine.unique_id()=b'\xe6ad\x08C\x13?&'(0xe661640843133f26)
>>> 
```

## 6. 　run()　pico上のプログラムを実行する

- pico上のプログラムを main.pyと同じように（`__name__ == '__main__'` として）実行する

### 実行例 <!-- omit in toc -->

```python
>>> .help
Available vREPL commands:
.cls/.clear - clear screen and prompt
.empty - clean vREPL
.ls - list files on Pico
.rtc - get the time form the onboard RTC
.sr - soft reset the Pico
.hr - hard reset the Pico
.gc - trigger garbage collector
.help - show this help
>>> .ls
['drivers', 'i2c_lcd.py', 'lcd_api.py.bak', 'lib', 'mymachine.py', 'ssd1306.py', 'ssd1331.py', 'ssd1331_ada.py']
>>> neos.run('mymachine.py')

# 以降、mymachine.py が __name__ == '__main__'　として実行される

```

## 7. 　delete_module()　importしたモジュールを削除する

- REPL上で、importしたモジュールを強制的に削除する
- REPL上で importしたモジュールのソースを変更する場合、再度同じモジュールを importしても変更が反映されない。REPL環境を再起動せずに変更を反映させるには、以下の手順が必要になる
  - 本関数を用いて importしたモジュールを強制的に削除する
  - pico上に変更したモジュールソースをアップロードする
  - REPL上から再度 importする
- 本関数の引数を省略すると、neosモジュールが削除される。他のモジュールを削除するときは引数にモジュール名の文字列を指定する


### 実行例 <!-- omit in toc -->

```python
>>> neos.delete_module()
try to delete modulename=neos

# neos.py をアップロードする

>>> import neos
>>> 
```

## 8. 　wlan_connect()　指定のワイヤレスネットワークに接続する

- 指定のワイヤレスネットワークに接続する
- 接続情報（SSID とパスワード）は、wlan_info.py の中に記述する

```python
# wlan_info.py
ssid = const("YOUR_SSID")           # 接続するWi-FiのSSID
passwd = const("YOUR_PASSWORD")     # 接続するWi-Fiのパスワード
```

### 実行例 <!-- omit in toc -->

```python
>>> neos.wlan_connect()
try to connect ssid=xxxxxxx-xxxxA-G passwd=xxxxxxxx
Connecting to Wi-Fi...
Connecting to Wi-Fi...
Connecting to Wi-Fi...
Connecting to Wi-Fi...
Connecting to Wi-Fi...
Connecting to Wi-Fi...
Connected to Wi-Fi
IP address: 192.168.0.xx
>>> 
```

## 9. 　wlan_isconnected()　ワイヤレスネットワークに接続されているかどうかを判断する

- 現在、ワイヤレスネットワークに接続されているかどうかを判断する

### 実行例 <!-- omit in toc -->

```python
>>> neos.wlan_isconnected()
wlan.isconnected()=True
>>> 
```

## 10. 　wlan_disconnect()　ワイヤレスネットワークから切断する

- 接続中のワイヤレスネットワークから切断する

### 実行例 <!-- omit in toc -->

```python
>>> neos.wlan_disconnect()
>>> neos.wlan_isconnected()
wlan.isconnected()=False
>>> 
```

## 11. 　wlan_scan()　利用可能なワイヤレスネットワークをスキャンする

- 結構便利

### 実行例 <!-- omit in toc -->

```python
>>> neos.wlan_scan()
(b'BCW710J-xxxxx-G', b'\xfcJ\xe90\x94\xe5', 1, -50, 7, 4)
(b'iPhone15', b'Nr\x8fl+\xeb', 1, -36, 5, 3)
(b'BCW710J-xxxxx-G', b'\xfcJ\xe90\x94\xc7', 6, -61, 7, 3)
>>> 
```

## 12. 　wlan_ifconfig()　IPアドレス、サブネットマスク、ゲートウェイ、DNSサーバーを取得する

- 見たとおり

### 実行例 <!-- omit in toc -->

```python
>>> neos.wlan_ifconfig()
IP address: 192.168.0.xx
('192.168.0.xx', '255.255.255.0', '192.168.0.1', '202.122.48.103')
>>> 
```

## 13. 　wlan_config()　ネットワークインターフェースパラメータを取得する

- 見たとおり

### 実行例 <!-- omit in toc -->

```python
>>> neos.wlan_config()
You must specify 'mac', 'ssid', 'channel', 'security', 'hostname'  or 'txpower' as a parameter.
>>> neos.wlan_config('mac')
wlan.config('mac')=b'(\xcd\xc1\tv,'(0x28cdc109762c)
>>> neos.wlan_config('ssid')
wlan.config('ssid')=BCW710J-xxxxx-G
>>> neos.wlan_config('channel')
wlan.config('channel')=1(0x1)
>>> neos.wlan_config('security')
wlan.config('security')=4194308(0x400004)
>>> neos.wlan_config('hostname')
wlan.config('hostname')=PicoW
>>> neos.wlan_config('txpower')
wlan.config('txpower')=31(0x1f)
>>> 
```
