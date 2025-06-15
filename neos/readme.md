![alt text](image/image06.jpg)
# neos モジュール
vREPL ターミナルから、接続された Raspberry Pi Pico / Pico W の状態を確認できる関数を提供するモジュールです。

[資材置き場topに戻る](../)

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
| readme.md                    | 本書                  |      | 2025/06/15 |      |
| [neos.md](neos.md)           | neosモジュール説明書  | 1.1  | 2025/06/15 |追加機能の説明を追加 |
| neos.py                      | neosモジュール本体    | 1.1  | 2025/06/15 |show_files()、set_ntp() 等追加 |
| [wlan_info.py](wlan_info.py) | Wi-Fi情報定義ファイル | 1.0  | 2025/03/30 |      |
