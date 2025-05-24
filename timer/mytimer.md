<a id="document_top"></a>

# mytimer モジュール説明書　 <!-- omit in toc -->

Raspberry Pi Pico W / Pico2 W 上で、machine.Timer() クラスに代わってタイマー制御を行うモジュールです。

<br>

## 対応機種とファームウェアバージョン <!-- omit in toc -->

- Raspberry Pi Pico W
  - ファームウェアバージョン： RPI_PICO_W-20241025-v1.24.0.uf2　以降
  - 上記以前のファームウェアでの動作は未確認です。

- Raspberry Pi Pico2 W
  - ファームウェアバージョン： RPI_PICO2_W-20250415-v1.25.0-preview.542.g9f3062799.uf2 以降
  - 上記以前のファームウェアでの動作は未確認です。

- Raspberry Pi Pico / Pico2
  - 動作する可能性は高いですが、試験は行っていません。

<br>

## ファイル一覧 <!-- omit in toc -->

| ファイル名 | ver.   | 日付       | 内容                 |
| ---------- | ------ | ---------- | -------------------- |
| mytimer.py | 作成中 | 2025/05/24 | モジュール本体       |
| mytimer.md | 作成中 | 2025/05/24 | ドキュメント（本書） |

<br>

## インストール方法 <!-- omit in toc -->

本モジュールは単独で使用するより、MyTimer() クラスを他のモジュールファイルに組み込んで使うことを想定しています。

<br>

## 使用方法 <!-- omit in toc -->

本モジュールから必要なクラスを `import` して使用します。

    from e_module import Edas, CheckTime

<br>

[ドキュメント先頭に戻る](#document_top)

<a id="method_list"></a>
## メソッド一覧 <!-- omit in toc -->

- [1. 　class MyTimer()](#1-class-mytimer)
  - [1.1. 　MyTimer()　新しいタイマーオブジェクトを作成する（コンストラクタ）](#11-mytimer新しいタイマーオブジェクトを作成するコンストラクタ)
  - [1.2. 　init()　タイマーを初期化する](#12-initタイマーを初期化する)
  - [1.3. 　deinit()　タイマーを停止する](#13-deinitタイマーを停止する)

<br>

[ドキュメント先頭に戻る](#document_top)

## 1. 　class MyTimer()

machine.Timer() クラスに代わってタイマー制御を行うモジュールです。

### 1.1. 　MyTimer()　新しいタイマーオブジェクトを作成する（コンストラクタ）

指定した id の新しいタイマーオブジェクトを構築します。

- MyTimer() クラスは、Raspberry Pi Pico の PIOを使用してタイマーを駆動します。
- id は PIOの処理ユニット（ステートマシン）の番号に使われ、0 ～ 7 の整数で指定します。

#### 書式： <!-- omit in toc -->

    <mytimer> = MyTimer(id=0)

<br>

### 1.2. 　init()　タイマーを初期化する

タイマーを初期化します。

#### 書式： <!-- omit in toc -->

    <mytimer>.init(mode=MyTimer.PERIODIC, period=10, callback=None)

#### 引数： <!-- omit in toc -->

| 名前     | 型         | 内容                                                   |
| -------- | ---------- | ----------------------------------------------------- |
| mode     | int        | MyTimer.PERIODIC を指定すると、タイマーを定期的に実行します。<br>MyTimer.ONE_SHOT を指定すると、タイマーを１回だけ実行します。 |
| period   | int        | タイマーの期間をミリ秒で指定します。                                                                                           |
| callback | (callable) | タイマー期間が終了したときに呼び出されるコールバックを指定します。                                                             |

- トレース情報出力レベルは [付録１ トレース情報出力レベル](e_module.md#appendix01)を参照してください。
<br>

### 1.3. 　deinit()　タイマーを停止する

タイマーを停止します。

#### 書式： <!-- omit in toc -->

    <mytimer>.deinit()

<br>

