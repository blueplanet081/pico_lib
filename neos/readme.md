![alt text](image/image06.jpg)
# neos モジュール
接続した Raspberry Pi Pico / Pico W の状態を vREPLから確認できる関数を提供するモジュールです。

<br>

## 使用例
#### 現在のメモリの使用状況を表示する

    >>> neos.show_memory_info()
    memory info:
    total:   191,424 bytes
    use:       8,400 bytes  (4.4%)
    remain:  183,024 bytes
    >>> 

#### MicroPythonのバージョン情報を表示する

    >>> neos.show_version()
    sys.version=3.4.0; MicroPython v1.23.0 on 2024-06-02
    >>> 

<br>

## ファイル一覧

| ファイル名                   | 内容                  | ver. | 日付       | メモ |
| ---------------------------- | --------------------- | ---- | ---------- | ---- |
| readme.md                    | 本書                  |      | 2025/04/29 |      |
| [neos.md](neos.md)           | neosモジュール説明書  | 1.0  | 2025/04/29 |      |
| neos.py                      | neosモジュール本体    | 1.0  | 2025/04/16 |      |
| [wlan_info.py](wlan_info.py) | Wi-Fi情報定義ファイル | 1.0  | 2025/03/30 |      |
