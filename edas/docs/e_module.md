# e_module モジュール　 <!-- omit in toc -->

Raspberry Pi Pico 上でシングルスレッドのマルチタスクを実現するための基本モジュールです。

<br>

## 対応機種とファームウェアバージョン <!-- omit in toc -->

- Raspberry Pi Pico W
  - ファームウェアバージョン： RPI_PICO_W-20241025-v1.24.0.uf2　以降
  - 上記以前のファームウェアでの動作は未確認です。

- Raspberry Pi Pico2 W
  - ファームウェアバージョン： RPI_PICO2_W-20250415-v1.25.0-preview.542.g9f3062799.uf2 以降
  - 上記以前のファームウェアでの動作は未確認です。

- Raspberry Pi Pico / Pico2
  - 動作する可能性は高いですが、試験はしていません。

<br>

## ファイル一覧 <!-- omit in toc -->

| ファイル名  | ver.   | 日付       | 内容                 |
| ----------- | ------ | ---------- | -------------------- |
| e_module.py | 作成中 | 2025/04/24 | モジュール本体       |
| e_module.md | 作成中 | 2025/04/24 | ドキュメント（本書） |

<br>

## インストール方法 <!-- omit in toc -->

本モジュールのファイルを、Pico / Pico W のルートディレクトリまたは lib ディレクトリ配下に格納してください。


    /
    └── lib
        └── e_module.py

<br>

## 使用方法 <!-- omit in toc -->

本モジュールから必要なクラスを `import` して使用します。

    from e_module import Edas, CheckTime

<br>

## メソッド一覧 <!-- omit in toc -->

- [1. 　class Edas()](#1-class-edas)
  - [1.1. 　start\_loop()　イベントループを開始する](#11-start_loopイベントループを開始する)
  - [1.2. 　stop\_loop()　イベントループを停止する](#12-stop_loopイベントループを停止する)
  - [1.3. 　Freezed()　イベントループを一時的に停止する](#13-freezedイベントループを一時的に停止する)
  - [1.4. 　Edas()　タスクを生成する（コンストラクタ）](#14-edasタスクを生成するコンストラクタ)
  - [1.5. 　start()　タスクを開始/再開する](#15-startタスクを開始再開する)
  - [1.6. 　pause()　タスクを中断する](#16-pauseタスクを中断する)
  - [1.7. 　stop() タスクを終了する](#17-stop-タスクを終了する)
  - [1.8. 　ticks\_ms() 　ハンドラーの現在の turnの時刻(msec)を取得する](#18-ticks_ms-ハンドラーの現在の-turnの時刻msecを取得する)
  - [1.9. 　y\_wait\_while() 　指定時間（msec）が経過するまで yieldを繰り返すタスクジェネレータ](#19-y_wait_while-指定時間msecが経過するまで-yieldを繰り返すタスクジェネレータ)
  - [1.10. 　after()　指定時間（秒）後に functionを実行する](#110-after指定時間秒後に-functionを実行する)
  - [1.11. 　after\_ms()　指定時間（msec）後に functionを実行する](#111-after_ms指定時間msec後に-functionを実行する)
  - [1.12. 　show\_edas()　動作中のタスクの一覧を表示するユーティリティメソッド](#112-show_edas動作中のタスクの一覧を表示するユーティリティメソッド)
  - [1.13. 　stop\_edas()　動作中のタスクを終了するユーティリティメソッド](#113-stop_edas動作中のタスクを終了するユーティリティメソッド)
  - [1.14. 　付録](#114-付録)
    - [1.14.1. 　付録１　トレース情報出力レベル](#1141-付録１トレース情報出力レベル)
    - [1.14.2. 　付録２　タスクの状態](#1142-付録２タスクの状態)
- [2. 　CheckTime()　経過時間(ミリ秒)をチェックするクラス](#2-checktime経過時間ミリ秒をチェックするクラス)
  - [2.1. 　CheckTime()　コンストラクタ](#21-checktimeコンストラクタ)
  - [2.2. 　set　基準時刻を trun時刻、または指定時刻に変更する](#22-set基準時刻を-trun時刻または指定時刻に変更する)
  - [2.3. 　add\_ms(delta)　基準時刻を delta(msec) だけ加算する](#23-add_msdelta基準時刻を-deltamsec-だけ加算する)
  - [2.4. 　ref\_time()　基準時刻を返す](#24-ref_time基準時刻を返す)
  - [2.5. 　y\_wait()　wait\_ms(msec) 時間が経過するまで yieldを繰り返す](#25-y_waitwait_msmsec-時間が経過するまで-yieldを繰り返す)
  - [2.6. 　wait(wait\_ms)　wait\_ms(msec) 時間が経過するまでTrue、経過したらFalseになる](#26-waitwait_mswait_msmsec-時間が経過するまでtrue経過したらfalseになる)

<br>
<br>

## 1. 　class Edas()

シングルスレッドでマルチタスク処理を行うためのイベントループとタスク管理機能を提供するクラスです。

### 1.1. 　start_loop()　イベントループを開始する

イベントループを開始するクラスメソッドです。

#### 書式： <!-- omit in toc -->

    Edas.start_loop(period=None, tracelevel=0)

#### 引数： <!-- omit in toc -->

| 名前       | 型  | 内容                                                                      |
| ---------- | --- | ------------------------------------------------------------------------- |
| period     | int, オプション | タイマーループの間隔をミリ秒単位で指定します。省略時は規定値、または現在の値が使用されます。 |
| tracelevel | int, オプション | トレース情報出力レベル（デバッグ用）を指定します。省略時は 0（出力しない）です。            |

- トレース情報出力レベルは [付録１ トレース情報出力レベル](#1141-付録１トレース情報出力レベル)を参照してください。

<br>

### 1.2. 　stop_loop()　イベントループを停止する

イベントループを停止するクラスメソッドです。

#### 書式： <!-- omit in toc -->

    Edas.stop_loop()

<br>

### 1.3. 　Freezed()　イベントループを一時的に停止する

イベントループを一時的に停止するためのコンテキストマネージャーです。タスクの状態更新を一時的に停止します。

停止する単位時間 (freezetime) をミリ秒単位で指定します。ブロック内の処理が freezetime 内に終了しない場合、単位時間を一区切りとして停止時間を延長します。単位時間のデフォルトは 5 ミリ秒です。

#### 書式： <!-- omit in toc -->

    with Edas.Freezed(freezetime=5):
        # フリーズ中に行う処理
        処理1
        処理2
        ...

<br>

### 1.4. 　Edas()　タスクを生成する（コンストラクタ）

バックグラウンドで動作するタスクを生成するコンストラクタです。

#### 書式： <!-- omit in toc -->

    <etask> = Edas(gen, name=None, previous_task=None, start=True):

#### 戻り値： <!-- omit in toc -->

作成したタスクオブジェクト（`<etask>`）。

#### 引数： <!-- omit in toc -->

| 名前          | 型           | 内容                                                   |
| ------------- | ------------ | ----------------------------------------------------- |
| gen           | ジェネレータ | タスクとして動作するジェネレータオブジェクト。               |
| name          | str, オプション    | タスクに付ける名前の文字列。省略時は自動的に名前が生成されます。 |
| previous_task | `<etask>`, オプション | 指定された場合、指定のタスクの終了後に新しいタスクが実行されます。 |
| start         | bool, オプション   | True（デフォルト）の場合、生成したタスクを即時開始します。False の場合は start() メソッドによる開始指示があるまで停止します。 |

<br>

### 1.5. 　start()　タスクを開始/再開する

開始指示待ちのタスク、または pause() で中断されたタスクを開始/再開します。

#### 書式：  <!-- omit in toc -->

    <etask>.start()

<br>

### 1.6. 　pause()　タスクを中断する

タスクを中断します。

sync=True を指定すると、タスクを同期ポイントで中断します。sync=False（デフォルト）の場合は、その場で中断します。中断したタスクは start() メソッドで再開できます。

#### 書式： <!-- omit in toc -->

    <etask>.pause(sync=False)

<br>

### 1.7. 　stop() タスクを終了する

タスクを終了します。

sync=True を指定すると、タスクを同期ポイントで終了します。sync=False（デフォルト）の場合は、その場で終了します。

#### 書式： <!-- omit in toc -->

    <etask>.stop(sync=False)

<br>

### 1.8. 　ticks_ms() 　ハンドラーの現在の turnの時刻(msec)を取得する

タイマーループの現在のターン開始時刻（ミリ秒）を取得するクラスメソッドです。

複数のタスク間で、同一ターンの同期を取る場合に使用します。

#### 書式： <!-- omit in toc -->

    <turn時刻> = Edas.ticks_ms()

<br>

### 1.9. 　y_wait_while() 　指定時間（msec）が経過するまで yieldを繰り返すタスクジェネレータ

指定時間（ミリ秒）が経過するまで yield を繰り返すタスクジェネレータです。

タスクジェネレータ内で時間調整をするために使用し、yield from 構文で呼び出します。

#### 書式： <!-- omit in toc -->

    yield from Edas.wait_while(wait_ms)

<br>

### 1.10. 　after()　指定時間（秒）後に functionを実行する

バックグラウンドで動作し、指定時間 (delay: float, 秒) 経過後に function を実行します。

作成したタスクオブジェクト (`<etask>`) を返します。

#### 書式： <!-- omit in toc -->

    <etask> = Edas.after(delay, function)

<br>

### 1.11. 　after_ms()　指定時間（msec）後に functionを実行する

動作は after() と同じですが、指定時間を秒ではなくミリ秒 (delay_ms: int) で指定します。

#### 書式： <!-- omit in toc -->

    <etask> = Edas.after_ms(delay_ms, function)

<br>

### 1.12. 　show_edas()　動作中のタスクの一覧を表示するユーティリティメソッド

現在動作しているタスクの一覧を vREPL上に表示するユーティリティメソッドです。

#### 書式（使い方）： <!-- omit in toc -->

    >>> from e_machine import Edas
    >>> Edas.show_edas()

<br>

### 1.13. 　stop_edas()　動作中のタスクを終了するユーティリティメソッド

現在動作しているタスクを終了するユーティリティメソッドです。

name に終了するタスクの名前を指定します。省略時はすべてのタスクを終了します。sync=True を指定した場合、タスクを同期ポイントまで待って終了します。

#### 書式（使い方）： <!-- omit in toc -->

    >>> from mymachine import Edas
    >>> Edas.stop_edas(name=None, sync=False)

<br>

### 1.14. 　付録

#### 1.14.1. 　付録１　トレース情報出力レベル

 [Edas.start_loop()](#11-start_loopイベントループを開始する) で指定する tracelevel に対応する出力内容です。指定した整数以下のレベルの情報が出力されます。<br>
 （例えば、tracelevel=15 を指定すると、0 ～ 15までのトレース情報が出力されます）


| tracelevel | 出力内容                 | 発生タイミング            |
| ---------- | ------------------------ | ------------------------- |
| 0          | メッセージ               | 随時                      |
| 8          | エラー等                 | エラー発生時                  |
| 11         | タスク生成               | Edas()処理時              |
| 11         | フリーズ処理             | with Edas.Freezed()処理時 |
| 14         | タスクの状態             | タスクの状態変更時        |
| 15         | SYNC終了                 | タスクのSYNC終了検出時    |
| 18         | SUNC検出                 | タスクのSYNC検出時        |
| 22         | turnタスク実行処理開始   | turn                      |
| 24         | turn整列処理開始         | turn                      |
| 28         | turn開始時間、終了時間等 | turn                      |
| 32         | 個々のタスクの開始情報   | turn中の各タスク開始時    |

<br>

#### 1.14.2. 　付録２　タスクの状態

| 状態    | 内部コード | 意味                    |
| ------- | ---------- | ----------------------- |
| NULL    | const(0)   | 無効                    |
| START   | const(1)   | 開始/再開（EXECに移行） |
| PAUSE   | const(2)   | 停止                    |
| EXEC    | const(3)   | 実行中                  |
| S_PAUSE | const(4)   | 実行中で SYNC停止待ち   |
| S_END   | const(5)   | 実行中で SYNC終了待ち   |
| END     | const(6)   | 終了（deleteに移行）    |


<br>
<br>

---

## 2. 　CheckTime()　経過時間(ミリ秒)をチェックするクラス

経過時間（ミリ秒）をチェックするためのクラスです。

### 2.1. 　CheckTime()　コンストラクタ

- CheckTimeオブジェクトを生成し、基準時刻を現在の turn時刻(msec)に設定する
- 注）turn時刻は Edasのタイマーループの各turnの開始時刻で、 Edas.ticks_ms() で得られる時刻

### 書式 <!-- omit in toc -->

    <ctime> = CheckTime()

<br>

### 2.2. 　set　基準時刻を trun時刻、または指定時刻に変更する

- ms はmsec単位の指定時刻。省略時は turn時刻になる
- 現在の基準時刻(msec)を返す

#### 書式 <!-- omit in toc -->

    <time_ms> = <ctime>.set(ms=None)

 <br>

### 2.3. 　add_ms(delta)　基準時刻を delta(msec) だけ加算する

- 基準時刻を delta(msec) だけ加算する
- 変更された現在の基準時刻(msec)を返す

#### 書式 <!-- omit in toc -->

    <time_ms> = <ctime>.add_ms(delta)

<br>

### 2.4. 　ref_time()　基準時刻を返す

- 現在の基準時刻(msec)を返す

#### 書式 <!-- omit in toc -->

    <time_ms> = <ctime>.ref_time()

<br>

### 2.5. 　y_wait()　wait_ms(msec) 時間が経過するまで yieldを繰り返す

- タスクジェネレータの中で、時間を調整するときに使用する
- update=Trueを指定すると、時間経過後に基準時刻を wait_ms分更新（加算）する<br>
省略時は、update=False（基準時刻を更新しない）

#### 書式（使用方法） <!-- omit in toc -->

    yield from <ctime>.y_wait(wait_ms, update=False)

#### 使用例 <!-- omit in toc -->

```python
import time
from machine import Pin
from mymachine import Edas, CheckTime

def lblink(pin, on_time, off_time, n):
    _ctime = CheckTime()
    _count = 0
    while not n or _count < n:
        pin.value(1)
        yield from _ctime.y_wait(on_time, update=True)
        pin.value(0)
        yield from _ctime.y_wait(off_time, update=True)
        _count += 1

led = Pin("LED", Pin.OUT)
Edas.start_loop()
Edas(lblink(led, 1000, 500, 5))

for i in range(10):
    print(f"---- round {i} ----")
    time.sleep_ms(3000)
```

<br>

### 2.6. 　wait(wait_ms)　wait_ms(msec) 時間が経過するまでTrue、経過したらFalseになる

- obsolete

#### 書式 <!-- omit in toc -->

    <True/False> = <ctime>.wait(wait_ms)

<br>

