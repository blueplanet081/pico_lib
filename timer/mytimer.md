<a id="document_top"></a>

# mytimer モジュール説明書　 <!-- omit in toc -->

Raspberry Pi Pico W / Pico2 W 上で、machine.Timer() クラスに代わってタイマー制御を行うモジュールです。

- machine.Timer() が他のタイマーと競合するときや、複数のタイマーを使いたいときに使います。
- StateMachineからの割り込みを使用します。周期の指定にかかわらず 1ミリ秒単位の割り込みを発生させて MicroPython側で時刻調整を行うので、それなりにオーバーヘッドは予想されます。

## メモ <!-- omit in toc -->

- Pico W の machine.Timer が、仮想タイマー（id=-1）しか使えないらしいので代替品を作った。
- 当初、StateMachineから 1ミリ秒単位の割り込みを発生させて設定期間分カウントする方式にしたら、負荷を掛けると割り込み周期が不安定になった（見掛け上？）ので、カウントをやめて割り込みごとに時刻を確認するように変更した。
- 方式変更でタイマーそのもののオーバーヘッドがちょっと大きくなったと思う。

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

| ファイル名        | ver.   | 日付       | 内容                     |
| ----------------- | ------ | ---------- | ------------------------ |
| mytimer.md        | 暫定版 | 2025/05/26 | ドキュメント（本書）     |
| mytimer.py        | 暫定版 | 2025/05/26 | モジュール本体           |
| mytimer_sample.py |        | 2025/05/26 | サンプルプログラム       |
| mytimer_old.py    | 旧版   | 2025/05/26 | 旧バージョン（お払い箱） |

<br>

## インストール方法 <!-- omit in toc -->

本モジュールは単独で使用するより、MyTimerクラスを他のモジュールファイルに組み込んで使うことを想定しています。


<br>

## 使用方法 <!-- omit in toc -->

本モジュールから MyTimerクラスを `import` して使用します。

    # サンプルプログラム
    from <組み込んだモジュール> import MyTimer


    # コールバック関数
    def callback1(timer):
        tm = time.ticks_ms()
        print(f"-> PIO triggered callback! {tm=}")


    timer1 = MyTimer(0)
    timer1.init(callback=callback1, period=1000, mode=MyTimer.PERIODIC)

    for i in range(5):
        print(f"---- round {i} ----")
        print(f"{time.ticks_ms()=}")
        time.sleep(10)

<br>

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

| 名前     | 型         | 内容                                                                                                                           |
| -------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------ |
| mode     | int        | MyTimer.PERIODIC を指定すると、タイマーを定期的に実行します。<br>MyTimer.ONE_SHOT を指定すると、タイマーを１回だけ実行します。 |
| period   | int        | タイマーの期間をミリ秒で指定します。                                                                                           |
| callback | (callable) | タイマー期間が終了したときに呼び出されるコールバックを指定します。                                                             |

- コールバックは１つの引数を取らなければならず、その引数にはタイマーオブジェクトが渡されます。

      # コールバック関数の例

      def callback0(timer):
          tm = time.ticks_ms()
          print(f"callback! {tm=}")
          self.former_tm = tm

          # 何らかの処理

          rt = time.ticks_diff(time.ticks_ms(), tm)
          timer.init(callback=callback0, period=(period - rt), mode=MyTimer.ONE_SHOT)

<br>

### 1.3. 　deinit()　タイマーを停止する

タイマーを停止します。

#### 書式： <!-- omit in toc -->

    <mytimer>.deinit()

<br>

