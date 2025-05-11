<a id="document_top"></a>

# e_machine モジュール説明書　 <!-- omit in toc -->

シングルスレッドでマルチタスクを実現する e_module の配下で、押しボタンや LED などの制御を行うためのモジュールです。



<br>

## 対応機種とファームウェアバージョン <!-- omit in toc -->

- Raspberry Pi Pico W
  - ファームウェアバージョン： RPI_PICO_W-20241025-v1.24.0.uf2　以降
  - 注意： RPI_PICO_W-20240602-v1.23.0.uf2 以前のファームウェアでは、以下の問題が確認されています。
    - Signalクラスのサブクラスから上位クラスのコンストラクタを呼び出した際に、キーワード引数がエラーになる。

- Raspberry Pi Pico2 W
  - ファームウェアバージョン： RPI_PICO2_W-20250415-v1.25.0-preview.542.g9f3062799.uf2 以降
  - 上記以前のファームウェアでの動作は未確認です。

- Raspberry Pi Pico / Pico2
  - 動作する可能性は高いですが、試験は行っていません。

<br>

## ファイル一覧 <!-- omit in toc -->

| ファイル名   | ver.   | 日付       | 内容                 |
| ------------ | ------ | ---------- | -------------------- |
| e_machine.py | 作成中 | 2025/04/24 | モジュール本体       |
| e_machine.md | 作成中 | 2025/05/02 | ドキュメント（本書） |

<br>

## インストール方法 <!-- omit in toc -->

本モジュールと e_module のファイルを、Pico / Pico W のルートディレクトリまたは lib ディレクトリ配下に格納してください。

    /
    └── lib
        └── e_module.py
            e_machine.py

<br>

## 使用方法 <!-- omit in toc -->

本モジュールから必要なクラスを import して使用します。

```python
# 使用例
import time
from e_machine import Eloop, Button, LED

led_0 = LED("LED")
btn_0 = Button(Bootsel_button(), name="Bootsel_button", hold_time=1.0,
                on_released=Mu(led_0.flicker, duty=0.8),
                on_held=led_0.off
                )

Eloop.start(loop_interval=10)
bloop = Button.start(period=100)

for i in range(1000):
    time.sleep_ms(1000)

```

<br>

[ドキュメント先頭に戻る](#document_top)

<a id="class_list"></a>

## クラス一覧 <!-- omit in toc -->

- [1. 　class Eloop()　マルチタスクを実行するクラス](#1-class-eloopマルチタスクを実行するクラス)
- [2. 　class Button()　押しボタンの状態を取得するクラス](#2-class-button押しボタンの状態を取得するクラス)
- [3. 　class Bootsel\_button()　bootselボタンを他のPin入力と同様に扱うためのクラス](#3-class-bootsel_buttonbootselボタンを他のpin入力と同様に扱うためのクラス)
- [4. 　class Mu()　Instant Closureクラス](#4-class-muinstant-closureクラス)
- [5. 　class LED()　LEDを制御するクラス](#5-class-ledledを制御するクラス)
- [6. 　class PWMLED()　LEDを PWMを用いて制御するクラス](#6-class-pwmledledを-pwmを用いて制御するクラス)

## メソッド一覧 <!-- omit in toc -->

- [1. 　class Eloop()　マルチタスクを実行するクラス](#1-class-eloopマルチタスクを実行するクラス)
  - [1.1. 　start()　イベントループを開始する（スタティックメソッド）](#11-startイベントループを開始するスタティックメソッド)
  - [1.2. 　stop()　イベントループを停止する（スタティックメソッド）](#12-stopイベントループを停止するスタティックメソッド)
  - [1.3. 　create\_task()　新しいタスクを生成し、イベントループに登録する（スタティックメソッド）](#13-create_task新しいタスクを生成しイベントループに登録するスタティックメソッド)
  - [1.4. 　resume()　タスクを再開する](#14-resumeタスクを再開する)
  - [1.5. 　pause()　タスクを中断する](#15-pauseタスクを中断する)
  - [1.6. 　cancel() タスクを終了する](#16-cancel-タスクを終了する)
  - [1.7. 　done() タスクの終了を判定する](#17-done-タスクの終了を判定する)
  - [1.8. 　result() タスクの実行結果を返す](#18-result-タスクの実行結果を返す)
  - [1.9. 　cancel\_basic\_tasks() 　動作中の全ての通常タスクを終了する（スタティックメソッド）](#19-cancel_basic_tasks-動作中の全ての通常タスクを終了するスタティックメソッド)
  - [1.10. 　wait\_for\_idle() 　動作中の全ての通常タスクの終了を待つ（スタティックメソッド）](#110-wait_for_idle-動作中の全ての通常タスクの終了を待つスタティックメソッド)
  - [1.11. 　idle\_time() 　通常のタスクが動いていない時間を取得する（スタティックメソッド）](#111-idle_time-通常のタスクが動いていない時間を取得するスタティックメソッド)
  - [1.12. 　Suspender()　with構文を使ってturnの開始を一時的に停止させる（内部クラス）](#112-suspenderwith構文を使ってturnの開始を一時的に停止させる内部クラス)
- [2. 　class Button()　押しボタンの状態を取得するクラス](#2-class-button押しボタンの状態を取得するクラス)
  - [2.1. 　start()　ボタン情報を取得するタスクを開始する（クラスメソッド）](#21-startボタン情報を取得するタスクを開始するクラスメソッド)
  - [2.2. 　idle\_time()　ボタンが操作されていない時間を取得する（クラスメソッド）](#22-idle_timeボタンが操作されていない時間を取得するクラスメソッド)
  - [2.3. 　str\_reason()　状態コード(reason)に対応する状態文字列を取得する（クラスメソッド）](#23-str_reason状態コードreasonに対応する状態文字列を取得するクラスメソッド)
  - [2.4. 　Button()　押しボタンを設定する（コンストラクタ）](#24-button押しボタンを設定するコンストラクタ)
  - [2.5. 　on\_action()　ボタン操作時のコールバック関数を設定する](#25-on_actionボタン操作時のコールバック関数を設定する)
  - [2.6. 　on\_pressed()　ボタン押下時のコールバック関数を設定する](#26-on_pressedボタン押下時のコールバック関数を設定する)
  - [2.7. 　on\_released()　ボタン解放時のコールバック関数を設定する](#27-on_releasedボタン解放時のコールバック関数を設定する)
  - [2.8. 　on\_held()　ボタン長押し時のコールバック関数を設定する](#28-on_heldボタン長押し時のコールバック関数を設定する)
  - [2.9. 付録](#29-付録)
    - [2.9.1. 　付録１　ボタンのモードの指定](#291-付録１ボタンのモードの指定)
    - [2.9.2. 　付録２　コールバック関数の呼び出し契機](#292-付録２コールバック関数の呼び出し契機)
    - [2.9.3. 　付録３　状態コード](#293-付録３状態コード)
    - [2.9.4. 　付録４　特別引数 myself](#294-付録４特別引数-myself)
    - [2.9.5. 　付録５　Button情報の取得](#295-付録５button情報の取得)
    - [2.9.6. 　付録６　トレース情報出力レベル](#296-付録６トレース情報出力レベル)
- [3. 　class Bootsel\_button()　bootsel ボタンを扱うためのクラス](#3-class-bootsel_buttonbootsel-ボタンを扱うためのクラス)
  - [3.1. 　Bootsel\_button()　bootselボタンを設定する（コンストラクタ）](#31-bootsel_buttonbootselボタンを設定するコンストラクタ)
  - [3.2. 　value()　bootsel ボタンの状態取得](#32-valuebootsel-ボタンの状態取得)
- [4. 　class Mu()　Instant Closureクラス](#4-class-muinstant-closureクラス)
  - [4.1. 　Mu()　クロージャーを生成する](#41-muクロージャーを生成する)
- [5. 　class LED()　LEDを制御するクラス](#5-class-ledledを制御するクラス)
  - [5.1. 　LED()　LEDを設定する（コンストラクタ）](#51-ledledを設定するコンストラクタ)
  - [5.2. 　on()　LEDを点灯する](#52-onledを点灯する)
  - [5.3. 　on\_for()　LEDを指定秒数点灯する](#53-on_forledを指定秒数点灯する)
  - [5.4. 　off()　LEDを消灯する](#54-offledを消灯する)
  - [5.5. 　toggle()　LEDの点灯と消灯を切り替える](#55-toggleledの点灯と消灯を切り替える)
  - [5.6. 　blink()　バックグラウンドで LEDを点滅させる](#56-blinkバックグラウンドで-ledを点滅させる)
  - [5.7. 　flicker()　バックグラウンドで LEDを点滅させる（blinkと引数の指定方法が違うだけ）](#57-flickerバックグラウンドで-ledを点滅させるblinkと引数の指定方法が違うだけ)
  - [5.8. 　y\_blink()　LEDを点滅させるタスクジェネレータ](#58-y_blinkledを点滅させるタスクジェネレータ)
  - [5.9. 　stop\_background()　バックグラウンド処理を停止する](#59-stop_backgroundバックグラウンド処理を停止する)
  - [5.10. 　stop\_background\_and\_execute()　バックグラウンド処理停止後に指定処理を実行する](#510-stop_background_and_executeバックグラウンド処理停止後に指定処理を実行する)
- [6. 　class PWMLED()　LEDを PWMを用いて制御するクラス](#6-class-pwmledledを-pwmを用いて制御するクラス)
  - [6.1. 　PWMLED()　PWMLEDを設定する（コンストラクタ）](#61-pwmledpwmledを設定するコンストラクタ)
  - [6.2. 　on()　PWMLEDを点灯する（duty比を最高値にする）](#62-onpwmledを点灯するduty比を最高値にする)
  - [6.3. 　off()　PWMLEDを消灯する（duty比を最低値にする）](#63-offpwmledを消灯するduty比を最低値にする)
  - [6.4. 　toggle()　現在の duty比を逆転する](#64-toggle現在の-duty比を逆転する)
  - [6.5. 　duty()　PWMの duty比を設定／取得する](#65-dutypwmの-duty比を設定取得する)
  - [6.6. 　value()　PWMの duty比を設定／取得する（duty() と同じ）](#66-valuepwmの-duty比を設定取得するduty-と同じ)
  - [6.7. 　fadein()　PWMの duty比を、現在値から最高値まで連続して変化させる](#67-fadeinpwmの-duty比を現在値から最高値まで連続して変化させる)
  - [6.8. 　fadeout()　PWMの duty比を現在値から最低値まで連続して変化させる](#68-fadeoutpwmの-duty比を現在値から最低値まで連続して変化させる)
  - [6.9. 　\_fade()　PWMの duty比を指定の値の間で連続して変化させる](#69-_fadepwmの-duty比を指定の値の間で連続して変化させる)
  - [6.10. 　y\_fade()　fadein、fadeout するためのタスクジェネレータ](#610-y_fadefadeinfadeout-するためのタスクジェネレータ)
  - [6.11. 　blink()　PWMLEDを点滅させる](#611-blinkpwmledを点滅させる)
  - [6.12. 　y\_blink()　PWMLED を点滅させるタスクジェネレータ](#612-y_blinkpwmled-を点滅させるタスクジェネレータ)
  - [6.13. 　pulse()　PWMLEDを連続して点滅させる](#613-pulsepwmledを連続して点滅させる)
  - [6.14. 　y\_pulse()　PWMLEDを連続して点滅させるタスクジェネレータ](#614-y_pulsepwmledを連続して点滅させるタスクジェネレータ)
  - [6.15. 　stop\_background()　バックグラウンド処理を停止する](#615-stop_backgroundバックグラウンド処理を停止する)
  - [6.16. 　stop\_background\_and\_execute()　バックグラウンド処理停止後に指定処理を実行する](#616-stop_background_and_executeバックグラウンド処理停止後に指定処理を実行する)

<br>
<br>

[ドキュメント先頭に戻る](#document_top)

---

## 1. 　class Eloop()　マルチタスクを実行するクラス

e_module の Edas() クラスをより使いやすくするためのラッパークラスです。

### 1.1. 　start()　イベントループを開始する（スタティックメソッド）

マルチタスク処理を行うイベントループを開始するスタティックメソッドです。

#### 書式： <!-- omit in toc -->

    Eloop.start(loop_interval=None, tracelevel=0)

#### 引数： <!-- omit in toc -->

| 名前          | 型              | 内容                                                |
| ------------- | --------------- | -------------------------------------------------- |
| loop_interval | int | タイマーループの間隔をミリ秒単位で指定します。省略時は規定値（100msec）、または現在の値が使用されます。 |
| tracelevel    | int | トレース情報出力レベル（デバッグ用）を指定します。省略時は 0（出力しない）です。   |

- トレース情報出力レベルは [e_module 説明書の、付録１ トレース情報出力レベル](e_module.md#appendix01)を参照してください。

<br>

### 1.2. 　stop()　イベントループを停止する（スタティックメソッド）

マルチタスク処理を行うイベントループを停止するスタティックメソッドです。

#### 書式： <!-- omit in toc -->

    Eloop.stop()

<br>

### 1.3. 　create_task()　新しいタスクを生成し、イベントループに登録する（スタティックメソッド）

バックグラウンドで動作するタスクを生成し、イベントループに登録するスタティックメソッドです。

#### 書式： <!-- omit in toc -->

    <etask> = Eloop.create_task(gen, name=None, previous_task=None, pause=False, terminate_by_sync=False, task_nature=BASIC):

#### 戻り値： <!-- omit in toc -->

生成されたタスクオブジェクト（`<etask>`）を返します。

#### 引数： <!-- omit in toc -->

| 名前              | 型           | 内容                                                |
| ----------------- | ------------ | -------------------------------------------------- |
| gen               | ジェネレータ | タスクとして動作するジェネレータオブジェクトです。                       |
| name              | str          | タスクに付ける名前の文字列です。省略時は適当な名前が自動的に生成されます。|
| previous_task     | `<etask>`    | 指定された場合、このタスクは指定されたタスクの終了後に実行されます。     |
| pause             | bool         | False（デフォルト）の場合、生成したタスクを即時開始します。True の場合は resume() メソッドによる開始指示があるまで停止します。 |
| terminate_by_sync | bool         | Truneの場合、タスクの終了時に 'SYNC'を待ちます。False（デフォルト）の場合は即時終了します。  |
| task_nature       | int          | タスクの性質を指定します。省略時は BASIC（通常のタスク）になります。  |

- タスクとして動作させるジェネレータオブジェクト、またはそのソースコードを以下では「タスクジェネレータ」と呼びます。

<br>

### 1.4. 　resume()　タスクを再開する

開始指示待ちのタスク、または pause() で中断されたタスクを開始/再開します。

#### 書式：  <!-- omit in toc -->

    <etask>.resume()

<br>

### 1.5. 　pause()　タスクを中断する

タスクを中断します。

sync=True（デフォルト）を指定すると、同期ポイントがあるタスクは同期ポイントまで実行して中断します。<br>
sync=False を指定すると、タスクは即時に中断します。<br>
（同期ポイントが無いタスクは、syncの指定にかかわらず即時に中断します。）

#### 書式： <!-- omit in toc -->

    <etask>.pause(sync=True)

<br>

### 1.6. 　cancel() タスクを終了する

タスクを終了します。

sync=True（デフォルト）を指定すると、同期ポイントがあるタスクは同期ポイントまで実行して終了します。<br>
sync=False を指定すると、タスクは即時に終了します。<br>
（同期ポイントが無いタスクは、syncの指定にかかわらず即時に終了します。）

#### 書式： <!-- omit in toc -->

    <etask>.cancel(sync=True)

<br>

### 1.7. 　done() タスクの終了を判定する

タスクが終了しているかどうかを判定します。<br>
タスクが終了していたら True、それ以外は Falseを返します。

#### 書式： <!-- omit in toc -->

    <bool> = <etask>.done()

<br>

### 1.8. 　result() タスクの実行結果を返す

タスクの実行結果（戻り値）を返します。<br>
タスクが終了していない、またはタスクに戻り値が無い場合は、Noneを返します。

#### 書式： <!-- omit in toc -->

    <return_value> = <etask>.result()

<br>

### 1.9. 　cancel_basic_tasks() 　動作中の全ての通常タスクを終了する（スタティックメソッド）

動作中の全ての通常タスク（task_nature=BASIC）を終了するスタティックメソッドです。

- sync=True（デフォルト）を指定すると、同期ポイントがあるタスクは同期ポイントまで実行して終了します。<br>
sync=False を指定すると、タスクは即時に終了します。<br>
（同期ポイントが無いタスクは、syncの指定にかかわらず即時に終了します。）
- 「BASIC」などのタスクの性質については、[付録３ タスクの性質](e_module.md#appendix03) を参照してください。

#### 書式： <!-- omit in toc -->

    Edas.cancel_basic_tasks(sync=False)

<br>

### 1.10. 　wait_for_idle() 　動作中の全ての通常タスクの終了を待つ（スタティックメソッド）

動作中の全ての通常タスク（task_nature=BASIC）と瞬間タスク（task_nature=FLASH）の終了を待つスタティックメソッドです。

- timeoutで指定した秒数まで終了しなかった場合は、それ以上待つことなくメソッドが終了します。
- 「BASIC」などのタスクの性質については、[付録３ タスクの性質](e_module.md#appendix03) を参照してください。

#### 書式： <!-- omit in toc -->

    Edas.wait_for_idle(timeout=1.0)

<br>

### 1.11. 　idle_time() 　通常のタスクが動いていない時間を取得する（スタティックメソッド）

イベントループ内で通常のタスク（task_nature=BASIC）が動作していない時間（秒）を取得するスタティックメソッドです。

Button などの常時動いている性質のタスクは無視します。

#### 書式： <!-- omit in toc -->

    <float> = Edas.idle_time()

<br>

### 1.12. 　Suspender()　with構文を使ってturnの開始を一時的に停止させる（内部クラス）

イベントループを一時的に停止し（タスクの状態更新も一時的に停止します）、特定の処理を割り込ませるためのコンテキストマネージャーです。Eloop()クラスの内部クラスになります。

停止する単位時間（freezetime）をミリ秒単位で指定します。単位時間のデフォルトは 5ミリ秒です。<br>
with ブロック内の処理が単位時間内に終了しない場合、単位時間毎に停止時間を延長します。

#### 使用例： <!-- omit in toc -->

```python
with Eloop.Suspender(freezetime=5):
    # 一時停止中に行う処理
    処理1
    処理2
    ...
```

<br>
<br>

[クラス一覧に戻る](#class_list)

---

## 2. 　class Button()　押しボタンの状態を取得するクラス

押しボタンの状態を監視し、あらかじめ設定された機能を実行するためのクラスです。<br>
（本クラスの機能はすべて、バックグラウンドタスクとして実行されます。）

### 2.1. 　start()　ボタン情報を取得するタスクを開始する（クラスメソッド）

ボタン情報を定期的に取得するバックグラウンドタスクを開始するクラスメソッドです。

#### 書式： <!-- omit in toc -->

    <etask> = Button.start(pull_up=None, name="Bloop", tracelevel=0, period=0)

### 引数： <!-- omit in toc -->

| 名前       | 型    | 内容                                                        |
| ---------- | ---- | ----------------------------------------------------------- |
| pull_up    | Bool | ボタンが pull_up設定かどうかのデフォルトを設定します。省略時は初期設定、または前回の設定が維持されます。  |
| name       | str  | バックグラウンドタスクの名前を設定します。省略した場合、"Bloop" が設定されます。         |
| tracelevel | int  | トレース情報の出力レベルを設定します（デバッグ用）。省略した場合、0（出力しない）となります。          |
| period     | int  | ボタンの状態をポーリングする間隔をミリ秒単位で指定します。省略した場合、初期設定（100 ミリ秒）または前回の設定が維持されます。 |

- トレース情報出力レベルの詳細については [付録６ トレース情報出力レベル](#286-付録６トレース情報出力レベル) を参照してください。

<br>

### 2.2. 　idle_time()　ボタンが操作されていない時間を取得する（クラスメソッド）

ボタンが最後に操作されてから現在までの時間（秒）を取得するクラスメソッドです。

#### 書式： <!-- omit in toc -->

    <float> = Button.idle_time()

<br>

### 2.3. 　str_reason()　状態コード(reason)に対応する状態文字列を取得する（クラスメソッド）

状態コード(reason)に対応する、状態を表す文字列を返すクラスメソッドです。

- 状態コードと状態を表す文字列の対応については、[付録３ 状態コード](#283-付録３状態コード) を参照してください。

#### 書式： <!-- omit in toc -->

    <str> = Button.str_reason(reason)

<br>

### 2.4. 　Button()　押しボタンを設定する（コンストラクタ）

指定された Pin、GPIO 番号、または Bootsel_button オブジェクトに対して、「押しボタン」オブジェクトを生成します。

#### 書式： <!-- omit in toc -->

    <button> = Button(pin, name="noname", pull_up=None,
                      hold_time=None, repeat_time=None,
                      on_action=None,
                      on_pressed=None,
                      on_released=None,
                      on_held=None)

#### 引数： <!-- omit in toc -->

| 名前        | 型                       | 内容                                            |
| ----------- | ------------------------ | ---------------------------------------------- |
| pin         | Pin, int, Bootsel_button | 割り当てる Pin オブジェクト、GPIO 番号、または Bootsel_button オブジェクトを指定します。          |
| name        | str      | ボタンの名前（任意）です。省略した場合、"noname" が設定されます。  |
| pull_up     | bool     | 押したときに Low になる場合は True を指定します。省略した場合、None（デフォルト設定）となります。 |
| hold_time   | float    | 長押し (HELD) および繰り返し (REPEATED) 開始までの遅延時間（秒）を設定します。   |
| repeat_time | float    | 繰り返し (REPEATED) の間隔（秒）を設定します。                 |
| on_action   | function | ボタンが操作された（押された、離された、長押しされた）ときに呼び出す関数を設定します。 |
| on_pressed  | function | ボタンが押されたときに呼び出す関数を設定します。           |
| on_released | function | ボタンが離されたときに呼び出す関数を設定します。           |
| on_held     | function | ボタンが長押しされたときに呼び出す関数を設定します。        |

<br>

- ボタンが「繰り返し押された（REPEATED）」場合は、その回数分「押された」場合の関数が呼び出されます。
- hold_time、repeat_time の指定によるボタンのモードについては、[付録１ ボタンのモードの指定](#281-付録１ボタンのモードの指定) を参照してください。
- on_xxxx による関数の呼び出し契機については、[付録２ ファンクションの呼び出し契機](#282-付録２ファンクションの呼び出し契機) を参照してください。
- 引数 on_xxxx= による関数の設定は、メソッド on_xxxx() によるものと同じですが、ここでは関数の引数を同時に設定することができません。関数の引数まで設定する場合は各メソッドを使用するか、[Mu() Instant Closureクラス](#4-class-muinstant-closureクラス) を併用してください。

<br>

### 2.5. 　on_action()　ボタン操作時のコールバック関数を設定する

ボタンが操作された（押された、離された、長押しされた）際に呼び出される関数を設定します。

- ボタンが「繰り返し押された（REPEATED）」場合は、その回数分「押された」ものとして関数が呼び出されます。

#### 書式： <!-- omit in toc -->

    <button>.on_action(func, *args, myself=True, **kwargs)

### 引数： <!-- omit in toc -->

| 名前     | 型            | 内容                                     |
| -------- | ------------- | ------------------------------------------------ |
| func     | function      | 呼び出す関数オブジェクトを指定します。           |
| *args    | 位置引数       | 関数に渡す位置引数を指定します。               |
| myself   | bool          | True（デフォルト）の場合、呼び出す関数に Button オブジェクト自身を最初の引数として渡します。 |
| **kwargs | キーワード引数 | 関数に渡すキーワード引数を指定します。                      |

<br>

### 2.6. 　on_pressed()　ボタン押下時のコールバック関数を設定する

ボタンが押されたときに呼び出される関数を設定します。

#### 書式： <!-- omit in toc -->

    <button>.on_pressed(func, *args, myself=None, **kwargs)

### 引数： <!-- omit in toc -->

| 名前     | 型             | 内容                                                  |
| -------- | ------------- | ----------------------------------------------------- |
| func     | function      | 呼び出す関数オブジェクトを指定します。                   |
| *args    | 位置引数       | 関数に渡す位置引数を指定します。                        |
| myself   | bool          | True の場合、呼び出す関数に Button オブジェクト自身を最初の引数として渡します。省略時は Falseとなります。 |
| **kwargs | キーワード引数 | 関数に渡すキーワード引数を指定します。                   |

<br>

### 2.7. 　on_released()　ボタン解放時のコールバック関数を設定する

ボタンが離されたときに呼び出される関数を設定します。

#### 書式： <!-- omit in toc -->

    <button>.on_released(func, *args, myself=None, **kwargs)

### 引数： <!-- omit in toc -->

| 名前     | 型             | 内容                                                  |
| -------- | ------------- | ----------------------------------------------------- |
| func     | function      | 呼び出す関数オブジェクトを指定します。                   |
| *args    | 位置引数       | 関数に渡す位置引数を指定します。                        |
| myself   | bool          | True の場合、呼び出す関数に Button オブジェクト自身を最初の引数として渡します。省略時は Falseとなります。 |
| **kwargs | キーワード引数 | 関数に渡すキーワード引数を指定します。                   |

<br>

### 2.8. 　on_held()　ボタン長押し時のコールバック関数を設定する

ボタンが長押しされたときに呼び出される関数を設定します。

#### 書式： <!-- omit in toc -->

    <button>.on_held(self, func, *args, myself=None, **kwargs)

### 引数： <!-- omit in toc -->

| 名前     | 型             | 内容                                                  |
| -------- | ------------- | ----------------------------------------------------- |
| func     | function      | 呼び出す関数オブジェクトを指定します。                   |
| *args    | 位置引数       | 関数に渡す位置引数を指定します。                        |
| myself   | bool          | True の場合、呼び出す関数に Button オブジェクト自身を最初の引数として渡します。省略時は Falseとなります。 |
| **kwargs | キーワード引数 | 関数に渡すキーワード引数を指定します。                   |

<br>
<br>

### 2.9. 付録

<a id="appendix01"></a>

#### 2.9.1. 　付録１　ボタンのモードの指定

ボタンの動作モードは、Button() コンストラクタ呼び出し時の hold_time および repeat_time 引数の設定によって決定されます。

| モード   | held_time | repeat_time | 備考                                         |
| ------- | --------- | ----------- | -------------------------------------------- |
| 通常     | なし      | なし        |                                               |
| 繰り返し | なし      | 指定あり    | repeat_timeで指定された間隔で繰り返し動作します。 |
| 繰り返し | 指定あり  | 指定あり    | 初回は held_time 経過後、以降は repeat_time で繰り返し動作します。 |
| 長押し   | 指定あり  | なし        | held_time で長押しを判定します。                |

<br>

<a id="appendix02"></a>

#### 2.9.2. 　付録２　コールバック関数の呼び出し契機

ボタン操作時にコールバック関数を呼び出すタイミングには、以下の 3 種類のモードがあります。<br>
（on_action で指定された関数は、すべての契機で呼び出されます。）

|     | モード   | コールバック関数 | 契機                                               |
| --- | -------- | ---------------- | -------------------------------------------------- |
| 1   | 通常     | on_pressed       | ボタンが押されたとき                               |
|     |          | on_released      | ボタンが離されたとき                               |
| 2   | 繰り返し | on_pressed       | ボタンが押されたとき                               |
|     |          | on_pressed       | ボタンが押され続けたとき（on_repeat は存在しない） |
|     |          | on_released      | ボタンが離されたとき                               |
| 3   | 長押し   | on_pressed       | ボタンが押されたとき                               |
|     |          | on_held          | ボタンが長押し後、離されたとき                     |
|     |          | on_released      | ボタンが長押しされずに離されたとき                 |

<br>

<a id="appendix03"></a>

#### 2.9.3. 　付録３　状態コード

プログラム内部で使用する状態コードと、状態を表す文字列の対応を示します。

| 状態コード | 状態を表す文字列 | 意味                                 |
| ---------- | ---------------- | ------------------------------------ |
| 0          | "NONE"           | ボタンが操作されていない状態です。   |
| 1          | "PRESSED"        | ボタンが押された状態です。           |
| 2          | "RELEASED"       | ボタンが離された状態です。           |
| 3          | "HELD"           | ボタンが長押しされた状態です。       |
| 4          | "REPEATED"       | ボタンが押し続けられている状態です。 |
| 5以上      | "unknown"        | 未定義の状態です。                   |

<br>

<a id="appendix04"></a>

#### 2.9.4. 　付録４　特別引数 myself

on_xxxx で指定するコールバック関数のキーワード引数に myself=True を指定すると、関数内で以下の情報を取得できます。

- myself=True を指定した場合、コールバック関数は **「最初の位置引数」** で myself引数を受け取る必要があります。
- on_action ではデフォルトで True、その他の on_xxxx ではデフォルトで False となります。

| 変数                 | 型        | 意味                                                 |
| -------------------- | -------- | ----------------------------------------------------- |
| myself               | オブジェクト | コールバック関数を呼び出した Button オブジェクトです。 |
| myself.name          | str      | ボタンの名前です。                                     |
| myself.reason        | int      | コールバック関数が呼び出された理由を示す状態コードです。   |
| myself.count         | int      | ボタンが押された回数です（REPEATED はカウントしません）。 |
| myself.repeat_count  | int      | 繰り返し (repeat) 回数です。                           |
| myself.interval_time | float    | 前回ボタンが押されてから今回押されるまでの時間（秒）です。 |
| myself.inactive_time | float    | 前回ボタンが離されてから今回押されるまでの時間（秒）です。 |
| myself.active_time   | float    | ボタンが押されてから離されるまでの時間（秒）です。        |

- 状態コードについては [付録３ 状態コード](#283-付録３状態コード) を参照してください。

<br>

<a id="appendix05"></a>

#### 2.9.5. 　付録５　Button情報の取得

外部から以下の情報を取得できます。

| 変数                  | 型   | 意味                                         |
| --------------------- | ---- | -------------------------------------------- |
| `<button>`.is_pressed | bool | ボタンが現在押されているかどうかを示します。 |

<br>

<a id="appendix06"></a>

#### 2.9.6. 　付録６　トレース情報出力レベル

Button.start() で指定する tracelevel に対応する出力内容です。指定した整数以下のレベルの情報が出力されます。<br>
（例えば、tracelevel=11 を指定すると、0 ～ 11までのトレース情報が出力されます。）

| tracelevel | 出力内容             | 発生タイミング                             |
| ---------- | -------------------- | ------------------------------------------ |
| 5          | ループ起動メッセージ | ボタン情報取得ループの起動時               |
| 10         | ボタン操作情報       | ボタンが操作されたとき                     |
| 11         | コールバック関数情報 | ボタン操作に対応する関数が呼び出されたとき |
| 22         | ループ情報           | ボタン情報の取得が実行されたとき           |

<br>
<br>

[クラス一覧に戻る](#class_list)

---

## 3. 　class Bootsel_button()　bootsel ボタンを扱うためのクラス

Raspberry Pi Pico W の bootsel ボタンを、通常の Pin 入力と同様に扱うためのクラスです。

### 3.1. 　Bootsel_button()　bootselボタンを設定する（コンストラクタ）

bootselボタンを設定します。

#### 書式： <!-- omit in toc -->

    <bootsel_button> = Bootsel_button()

#### 使用例： <!-- omit in toc -->

```python
btn_0 = Button(Bootsel_button(), name="Bootsel_button", hold_time=1.0,
                on_released=led_0.flicker,
                on_held=led_0.off
                )
```

<br>

### 3.2. 　value()　bootsel ボタンの状態取得

bootsel ボタンが押されている場合は 1 を、押されていない場合は 0 を返します。ていたら 1、押されていなかったら 0 を返す。

### 書式： <!-- omit in toc -->

    <int> = <bootsel_button>.value()

<br>
<br>

[クラス一覧に戻る](#class_list)

---

## 4. 　class Mu()　Instant Closureクラス

普通の関数(func)をクロージャーとして埋め込むクラスの MicroPythonバージョンです。

- Button() の引数としてコールバック関数を渡すときに、その関数に渡す引数も同時に定義するために使用します。

### 4.1. 　Mu()　クロージャーを生成する

クロージャーを生成します。

#### 書式： <!-- omit in toc -->

    <closure_func> = Mu(func, *args, **kwargs)

### 引数： <!-- omit in toc -->

| 名前     | 型       | 内容                                           |
| -------- | -------- | ---------------------------------------------- |
| func     | function | 埋め込む関数オブジェクトを指定します。         |
| *args    | tuple    | 埋め込む関数に渡す位置引数を指定します。       |
| **kwargs | dict     | 埋め込む関数に渡すキーワード引数を指定します。 |

#### 使用例： <!-- omit in toc -->

```python
    btn_ledR = Button(6, name="Btn_ledR", hold_time=1.0,
                      on_released=Mu(ledR.blink, on_time=1.0, off_time=0.2),
                      on_held=ledR.stop_background
                      )
```

<br>
<br>

[クラス一覧に戻る](#class_list)

---

## 5. 　class LED()　LEDを制御するクラス

LEDを制御するためのクラスです。（Signalクラスのサブクラスになります。）

### 5.1. 　LED()　LEDを設定する（コンストラクタ）

LED が接続されたGPIO番号、または内蔵LEDに対して LED オブジェクトを作成するコンストラクタです。

#### 書式： <!-- omit in toc -->

    <led> = LED(pno, value=0, invert=False)

割り当てる Pin オブジェクト、GPIO 番号、または Bootsel_button オブジェクトを指定します。          |

#### 引数： <!-- omit in toc -->

| 名前   | 型       | 内容                                                                |
| ------ | -------- | ------------------------------------------------------------------ |
| pno    | int, str | LEDが接続された GPIO番号、または "led" を指定します。                  |
| value  | int      | LEDの初期値を指定します。（消灯のときは 0（デフォルト）、点灯のときは 1 を指定します。） |
| invert | bool     | LEDの接続が正論理の場合は False（デフォルト）、負論理の場合は Trueを指定します。|

- pinが highの時に LEDが点灯する状態を「正論理」、lowの時に LEDが点灯する状態を「負論理」と言います。

<br>

### 5.2. 　on()　LEDを点灯する

LEDを点灯します。blink などのバックグラウンド処理が実行中の場合は、それらを先に停止します。

#### 書式： <!-- omit in toc -->

    <led>.on()

<br>

### 5.3. 　on_for()　LEDを指定秒数点灯する

LEDを点灯し、指定(seconds)秒後に消灯します。blink などのバックグラウンド処理が実行中の場合は、それらを先に停止します。

- seconds が 0以下の場合は on() と同じ動作になります。（点灯し、自動では消灯しません。）

#### 書式： <!-- omit in toc -->

    <led>.on_for(seconds=0)

<br>

### 5.4. 　off()　LEDを消灯する

LEDを消灯します。blink などのバックグラウンド処理が実行中の場合は、それらを先に停止します。

#### 書式 <!-- omit in toc -->

    <led>.off()

<br>

### 5.5. 　toggle()　LEDの点灯と消灯を切り替える

LEDの現在の点灯状態を反転させます。

#### 書式： <!-- omit in toc -->

    <led>.toggle()

<br>

### 5.6. 　blink()　バックグラウンドで LEDを点滅させる

バックグラウンドで LEDを点滅させます。他のバックグラウンド処理が実行中の場合は、それらを先に停止します。

#### 書式： <!-- omit in toc -->

    <etask> = <led>.blink(on_time=1.0, off_time=1.0, n=None, previous_task=None)

#### 引数一覧 <!-- omit in toc -->

| 名前          | 型              | 内容                                  |
| ------------- | --------------- | ------------------------------------ |
| on_time       | float           | LED の点灯時間（秒）を指定します。      |
| off_time      | float           | LED の消灯時間（秒）を指定します。      |
| n             | int, None       | 点滅回数を指定します。0 または None を指定すると、永久に繰り返します。         |
| previous_task | `<etask>`, None | 指定された場合、先行するタスク（`<etask>`）の終了後にこの点滅処理を実行します。 |

<br>

### 5.7. 　flicker()　バックグラウンドで LEDを点滅させる（blinkと引数の指定方法が違うだけ）

バックグラウンドで LED を点滅させます。他のバックグラウンド処理が実行中の場合は、それらを先に停止します。<br>
（blinke と引数の指定方法が違うだけで、同様の処理になります。）

#### 書式： <!-- omit in toc -->

    <etask> = <led>.flicker(interval=1.0, duty=0.5, n=None, previous_task=None)

#### 引数： <!-- omit in toc -->

| 名前          | 型         | 内容                                                   |
| ------------- | --------- | ------------------------------------------------------ |
| interval      | float     | 点滅の周期（秒）を指定します。                            |
| duty          | float     | 点滅周期に対する点灯時間の割合を指定します。0.5 の場合、点灯時間と消灯時間が等しくなります（デフォルト）。     |
| n             | int       | 点滅回数を指定します。0 または None を指定すると、永久に繰り返します。   |
| previous_task | `<etask>` | 指定された場合、先行するタスク（`<etask>`）の終了後にこの点滅処理を実行します。 |

<br>

### 5.8. 　y_blink()　LEDを点滅させるタスクジェネレータ

#### 書式： <!-- omit in toc -->

    <generator> = <led>.y_blink(on_time, off_time, n)

#### 引数： <!-- omit in toc -->

| 名前     | 型         | 内容                                          |
| -------- | ---------- | --------------------------------------------- |
| on_time  | float      | LED の点灯時間（秒）を指定します。     |
| off_time | float      | LED の消灯時間（秒）を指定します。           |
| n        | int        | 点滅回数を指定します。0 または None を指定すると、永久に繰り返します。 |

<br>

### 5.9. 　stop_background()　バックグラウンド処理を停止する

blinkなどのバックグラウンド処理を停止します。

- sync=True を指定すると、バックグラウンド処理を同期ポイントまで実行した後停止します。False の場合は即座に停止します（省略時のデフォルトは True です）。

#### 書式： <!-- omit in toc -->

    <led>.stop_background(sync=True)

<br>

### 5.10. 　stop_background_and_execute()　バックグラウンド処理停止後に指定処理を実行する

blink などのバックグラウンド処理を停止した後、指定された関数 func を実行します。

- sync=True を指定すると、バックグラウンド処理を同期ポイントまで実行した後停止します。False の場合は即座に停止します（省略時のデフォルトは False です）。

#### 書式： <!-- omit in toc -->

    <led>._after_background(func, sync=False)

<br>
<br>

[クラス一覧に戻る](#class_list)

---

## 6. 　class PWMLED()　LEDを PWMを用いて制御するクラス

PWM (Pulse Width Modulation) を用いて LED を制御するためのクラスです (`PWM` クラスのサブクラスです)。

### 6.1. 　PWMLED()　PWMLEDを設定する（コンストラクタ）

LED が接続された GPIO 番号、Pin オブジェクト、または `LED` オブジェクトに対して `PWMLED` オブジェクトを作成するコンストラクタです。

#### 書式： <!-- omit in toc -->

    <pwmled> = PWMLED(pin, freq=100, value=0.0, lo=0.0, hi=1.0, invert=False, curve=1.0)

#### 引数： <!-- omit in toc -->

| 名前   | 型            | 内容                                                   |
| ------ | ------------- | ----------------------------------------------------- |
| pin    | int, LED, pin | 対象のpinを、pin番号(int)、 LED、 Pin などで指定します。     |
| freq   | int     | PWM出力の周波数(Hz)を指定します。省略時は 100Hzになります。            |
| value  | float   | PWM出力のduty比率の初期時を 0.0～1.0の値で指定します。省略時は 0.0になります。|
| lo     | float   | PWM出力のduty比率の最低値を指定します。省略時は 0.0になります。        |
| hi     | float   | PWM出力のduty比率の最高値を指定します。省略時は 1.0になります。        |
| invert | bool    | LEDの接続が正論理の場合は False（デフォルト）、負論理の場合は Trueを指定します。  |
| curve  | float   | duty比率の指定値と物理値の対数カーブを指定します。1.0より大きい値を指定すると、duty比率に対する LEDの明るさ変化が「緩やか」になります。省略値は 1.0になります。|

- pinが highの時に LEDが点灯する状態を「正論理」、lowの時に LEDが点灯する状態を「負論理」と言います。

- 対数カーブに指定する値
  - curve ＜ 1.0： 「Cカーブ」相当
  - curve=1.0： リニア（ 「Bカーブ」相当）
  - curve=1.5 ～ 2.5： volumeで言う「Aカーブ」相当
  - curve ＞ 2.5： 「Dカーブ」とかなんとか

<br>

### 6.2. 　on()　PWMLEDを点灯する（duty比を最高値にする）

PWMLEDを点灯します（duty比を最高値にします）。<br>
バックグラウンド処理が実行中の場合は、それらを先に停止します。

#### 書式： <!-- omit in toc -->

    <pwmled>.on()

<br>

### 6.3. 　off()　PWMLEDを消灯する（duty比を最低値にする）

PWMLEDを消灯します（duty比を最低値にします）。<br>
バックグラウンド処理が実行中の場合は、それらを先に停止します。

#### 書式： <!-- omit in toc -->

    <pwmled>.off()

<br>

### 6.4. 　toggle()　現在の duty比を逆転する

PWMLEDの現在の duty比を逆転させます。

#### 書式： <!-- omit in toc -->

    <pwmled>.toggle()

<br>

### 6.5. 　duty()　PWMの duty比を設定／取得する

PWMの duty比（value）を 0.0～1.0 の範囲で設定します。引数を省略した場合は、現在の duty比を返します。

#### 書式： <!-- omit in toc -->


    <float> = <pwmled>.duty(value=None)

<br>

### 6.6. 　value()　PWMの duty比を設定／取得する（duty() と同じ）

PWMの duty比（value）を 0.0～1.0 の範囲で設定します。引数を省略した場合は、現在の duty比を返します。
（機能は duty() と同じです。）

#### 書式： <!-- omit in toc -->

    <float> = <pwmled>.value(value=None)

<br>

### 6.7. 　fadein()　PWMの duty比を、現在値から最高値まで連続して変化させる

PWMの duty比を、現在値から最高値まで fade_time 秒かけて変化させます。<br>
バックグラウンド処理が実行中の場合は、それらを先に停止します。

#### 書式： <!-- omit in toc -->

    <etask> = <pwmled>.fadein(fade_time=1.0)

<br>

### 6.8. 　fadeout()　PWMの duty比を現在値から最低値まで連続して変化させる

PWM の duty 比を、現在値から最低値まで fade_time 秒かけて連続的に変化させます。<br>
バックグラウンド処理が実行中の場合は、それらを先に停止します。

#### 書式： <!-- omit in toc -->

    <etask> = <pwmled>.fadeout(fade_time=1.0)

<br>

### 6.9. 　_fade()　PWMの duty比を指定の値の間で連続して変化させる

PWM の duty 比を、指定された開始 duty 比 (duty_from) から終了 duty 比 (duty_to) まで fade_time 秒かけて連続的に変化させます。

- fadein()、fadeout() から呼び出される内部関数です。

#### 書式： <!-- omit in toc -->

    <etask> = <pwmled>._fade(fade_time, duty_from=0.0, duty_to=1.0)

<br>

### 6.10. 　y_fade()　fadein、fadeout するためのタスクジェネレータ

#### 書式： <!-- omit in toc -->

    <generator> = <pwmled>.y_fade(fade_time, duty_from, duty_to)

<br>

### 6.11. 　blink()　PWMLEDを点滅させる

PWMLED を、duty比の最低値から最高値の間で点滅させます。必要に応じて、点灯開始時と点灯終了時に fade-in/fade-out を実行します。<br>
他のバックグラウンド処理が実行中の場合は、それらを先に停止します。

#### 書式： <!-- omit in toc -->

    <etask> = <pwmled>.blink(on_time=1.0, off_time=1.0, fade_in_time=0.0, fade_out_time=0.0, n=None)

#### 引数： <!-- omit in toc -->

| 名前          | 型        | 内容                                           |
| ------------- | --------- | --------------------------------------------- |
| on_time       | float     | 点灯時間（秒）を指定します。省略時のデフォルトは 1.0 秒です。       |
| off_time      | float     | 消灯時間（秒）を指定します。省略時のデフォルトは 1.0 秒です。        |
| fade_in_time  | float     | 点灯開始時に、duty比を最低値から最高値まで変化させる時間（秒）を指定します。省略時のデフォルトは 0.0 秒です。 |
| fade_out_time | float     | 点灯終了時に、duty比を最高値から最低値まで変化させる時間（秒）を指定します。省略時のデフォルトは 0.0 秒です。 |
| n             | int | 点滅回数を指定します。0 または None を指定すると、永久に繰り返します。 |

<br>

### 6.12. 　y_blink()　PWMLED を点滅させるタスクジェネレータ

#### 書式： <!-- omit in toc -->

    <generator> = <pwmled>.y_blink(on_time, off_time, fade_in_time, fade_out_time, n)

<br>

### 6.13. 　pulse()　PWMLEDを連続して点滅させる

PWMLED を、duty比の最低値から最高値の間で連続して点滅させます。必要に応じて、点灯開始時と点灯終了時に fade-in/fade-out を実行します。<br>
他のバックグラウンド処理が実行中の場合は、それらを先に停止します。

#### 書式： <!-- omit in toc -->

    <etask> = <pwmled>.pulse(fade_in_time=1.0, fade_out_time=1.0, n=None)

#### 引数： <!-- omit in toc -->

| 名前          | 型        | 内容                                           |
| ------------- | --------- | --------------------------------------------- |
| fade_in_time  | float     | 点灯開始時に、duty比を最低値から最高値まで変化させる時間（秒）を指定します。省略時のデフォルトは 0.0 秒です。 |
| fade_out_time | float     | 点灯終了時に、duty比を最高値から最低値まで変化させる時間（秒）を指定します。省略時のデフォルトは 0.0 秒です。 |
| n             | int | 点滅回数を指定します。0 または None を指定すると、永久に繰り返します。 |

<br>

### 6.14. 　y_pulse()　PWMLEDを連続して点滅させるタスクジェネレータ

#### 書式： <!-- omit in toc -->

    <generator> = <pwmled>.y_pulse(fade_in_time, fade_out_time, n)

<br>

### 6.15. 　stop_background()　バックグラウンド処理を停止する

blinkや fadein などのバックグラウンド処理を停止します。

- sync=True を指定すると、バックグラウンド処理を同期ポイントまで実行した後停止します。False の場合は即座に停止します（省略時のデフォルトは True です）。

#### 書式： <!-- omit in toc -->

    <pwmled>.stop_background(sync=True)

<br>

### 6.16. 　stop_background_and_execute()　バックグラウンド処理停止後に指定処理を実行する

- blinkや fadein などのバックグラウンド処理を停止した後、指定された関数 func を実行します。
- sync=True を指定すると、バックグラウンド処理を同期ポイントまで実行した後停止します。False の場合は即座に停止します（省略時のデフォルトは False です）。

#### 書式： <!-- omit in toc -->

    <pwmled>._after_background(func, sync=False)

<br>

[クラス一覧に戻る](#class_list)
