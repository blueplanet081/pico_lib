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

| ファイル名   | ver. | 日付       | 内容                 |
| ------------ | ---- | ---------- | -------------------- |
| e_machine.py |作成中| 2025/04/24 | モジュール本体       |
| e_machine.md |作成中| 2025/04/24 | ドキュメント（本書） |

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

## クラス一覧 <!-- omit in toc -->

- [1. 　class Eloop()　マルチタスクを実行するクラス](#1-class-eloopマルチタスクを実行するクラス)
- [2. 　class Button()　押しボタンの状態を取得するクラス](#2-class-button押しボタンの状態を取得するクラス)
- [3. 　class Bootsel\_button()　bootselボタンを他のPin入力と同様に扱うためのクラス](#3-class-bootsel_buttonbootselボタンを他のpin入力と同様に扱うためのクラス)
- [4. 　class Mu()　Instant Closureクラス](#4-class-muinstant-closureクラス)
- [5. 　class LED()　LEDを制御するクラス](#5-class-ledledを制御するクラス)
- [6. 　class PWMLED()　LEDを PWMを用いて制御するクラス](#6-class-pwmledledを-pwmを用いて制御するクラス)


## メソッド一覧 <!-- omit in toc -->

- [1. 　class Eloop()　マルチタスクを実行するクラス](#1-class-eloopマルチタスクを実行するクラス)
  - [1.1. 　start()　イベントループを開始する](#11-startイベントループを開始する)
  - [1.2. 　stop()　イベントループを停止する](#12-stopイベントループを停止する)
  - [1.3. 　create\_task()　新しいタスクを生成し、イベントループに登録する](#13-create_task新しいタスクを生成しイベントループに登録する)
  - [1.4. 　start()　タスクを開始/再開する](#14-startタスクを開始再開する)
  - [1.5. 　pause()　タスクを中断する](#15-pauseタスクを中断する)
  - [1.6. 　stop()　タスクを終了する](#16-stopタスクを終了する)
  - [1.7. 　Suspender()　with構文を使ってturnの開始を一時的に停止させる（サブクラス）](#17-suspenderwith構文を使ってturnの開始を一時的に停止させるサブクラス)
- [2. 　class Button()　押しボタンの状態を取得するクラス](#2-class-button押しボタンの状態を取得するクラス)
  - [2.1. 　start()　ボタン情報を取得するタスクを開始する](#21-startボタン情報を取得するタスクを開始する)
  - [2.2. 　str\_reason()　状態コード(reason)に対応する状態文字列の取得](#22-str_reason状態コードreasonに対応する状態文字列の取得)
  - [2.3. 　Button()　押しボタンを設定する（コンストラクタ）](#23-button押しボタンを設定するコンストラクタ)
  - [2.4. 　on\_action()　ボタンが操作されたときに呼び出すファンクションを設定する](#24-on_actionボタンが操作されたときに呼び出すファンクションを設定する)
  - [2.5. 　on\_pressed()　ボタンが押されたときに呼び出すファンクションを設定する](#25-on_pressedボタンが押されたときに呼び出すファンクションを設定する)
  - [2.6. 　on\_released()　ボタンが離されたときに呼び出すファンクションを設定する](#26-on_releasedボタンが離されたときに呼び出すファンクションを設定する)
  - [2.7. 　on\_held()　ボタンが長押しされたときに呼び出すファンクションを設定する](#27-on_heldボタンが長押しされたときに呼び出すファンクションを設定する)
  - [2.8. 付録](#28-付録)
    - [2.8.1. 　付録１　ボタンのモードの指定](#281-付録１ボタンのモードの指定)
    - [2.8.2. 　付録２　ファンクションの呼び出し契機](#282-付録２ファンクションの呼び出し契機)
    - [2.8.3. 　付録３　状態コード](#283-付録３状態コード)
    - [2.8.4. 　付録４　特別引数 myself](#284-付録４特別引数-myself)
    - [2.8.5. 　付録５　Button情報の取得](#285-付録５button情報の取得)
    - [2.8.6. 　付録６　トレース情報出力レベル](#286-付録６トレース情報出力レベル)
- [3. 　class Bootsel\_button()　bootselボタンを他のPin入力と同様に扱うためのクラス](#3-class-bootsel_buttonbootselボタンを他のpin入力と同様に扱うためのクラス)
  - [3.1. 　Bootsel\_button()　bootselボタンを設定する（コンストラクタ）](#31-bootsel_buttonbootselボタンを設定するコンストラクタ)
  - [3.2. 　value()　bootsel\_buttonの状態を返す](#32-valuebootsel_buttonの状態を返す)
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
  - [5.10. 　stop\_background\_and\_execute()　バックグラウンド処理を停止した後、指定処理を実行する](#510-stop_background_and_executeバックグラウンド処理を停止した後指定処理を実行する)
- [6. 　class PWMLED()　LEDを PWMを用いて制御するクラス](#6-class-pwmledledを-pwmを用いて制御するクラス)
  - [6.1. 　PWMLED()　PWMLEDを設定する（コンストラクタ）](#61-pwmledpwmledを設定するコンストラクタ)
  - [6.2. 　on()　PWMLEDを点灯する（duty比を最高値にする）](#62-onpwmledを点灯するduty比を最高値にする)
  - [6.3. 　off()　PWMLEDを消灯する（duty比を最低値にする）](#63-offpwmledを消灯するduty比を最低値にする)
  - [6.4. 　toggle()　現在の duty比を逆転する](#64-toggle現在の-duty比を逆転する)
  - [6.5. 　duty()　PWMの duty比率を設定／取得する](#65-dutypwmの-duty比率を設定取得する)
  - [6.6. 　value()　PWMの duty比率を設定／取得する（duty() と同じ）](#66-valuepwmの-duty比率を設定取得するduty-と同じ)
  - [6.7. 　fadein()　PWMの duty比を、現在値から最高値まで連続して変化させる](#67-fadeinpwmの-duty比を現在値から最高値まで連続して変化させる)
  - [6.8. 　fadeout()　PWMの duty比を現在値から最低値まで連続して変化させる](#68-fadeoutpwmの-duty比を現在値から最低値まで連続して変化させる)
  - [6.9. 　\_fade()　PWMの duty比を指定の開始 duty比から指定の終了 duty比まで連続して変化させる](#69-_fadepwmの-duty比を指定の開始-duty比から指定の終了-duty比まで連続して変化させる)
  - [6.10. 　y\_fade()　fadein、fadeout するためのタスクジェネレータ](#610-y_fadefadeinfadeout-するためのタスクジェネレータ)
  - [6.11. 　blink()　PWMLEDを点滅させる](#611-blinkpwmledを点滅させる)
  - [6.12. 　y\_blink()　PWMLED を点滅させるタスクジェネレータ](#612-y_blinkpwmled-を点滅させるタスクジェネレータ)
  - [6.13. 　pulse()　PWMLEDを連続して点滅させる](#613-pulsepwmledを連続して点滅させる)
  - [6.14. 　y\_pulse()　PWMLEDを連続して点滅させるタスクジェネレータ](#614-y_pulsepwmledを連続して点滅させるタスクジェネレータ)
  - [6.15. 　stop\_background()　バックグラウンド処理を停止する](#615-stop_backgroundバックグラウンド処理を停止する)
  - [6.16. 　stop\_background\_and\_execute()　バックグラウンド処理を停止した後、指定処理を実行する](#616-stop_background_and_executeバックグラウンド処理を停止した後指定処理を実行する)

<br>
<br>

---

## 1. 　class Eloop()　マルチタスクを実行するクラス

e_module の Edas() クラスをより使いやすくするためのラッパークラスです。

### 1.1. 　start()　イベントループを開始する

マルチタスク処理を行うイベントループを開始するスタティックメソッドです。

#### 書式： <!-- omit in toc -->

    Eloop.start(loop_interval=None, tracelevel=0)

#### 引数： <!-- omit in toc -->

| 名前          | 型        | 内容                                                                      |
| ------------- | --------- | ------------------------------------------------------------------- |
| loop_interval | int, オプション | タイマーループの間隔をミリ秒単位で指定します。省略時は規定値（100msec）、または現在の値が使用されます。 |
| tracelevel    | int, オプション | トレース情報出力レベル（デバッグ用）を指定します。省略時は 0（出力しない）です。   |

<br>

### 1.2. 　stop()　イベントループを停止する

マルチタスク処理を行うイベントループを停止するスタティックメソッドです。

#### 書式： <!-- omit in toc -->

    Eloop.stop()

<br>

### 1.3. 　create_task()　新しいタスクを生成し、イベントループに登録する

バックグラウンドで動作するタスクを生成し、イベントループに登録するスタティックメソッドです。

#### 書式： <!-- omit in toc -->

    <etask> = Eloop.create_task(gen, name=None, previous_task=None, start=True):

#### 戻り値： <!-- omit in toc -->

生成されたタスクオブジェクト（`<etask>`）を返します。

#### 引数： <!-- omit in toc -->

| 名前          | 型           | 内容                                                        |
| ------------- | ------------ | ---------------------------------------------------------- |
| gen           | ジェネレータ | タスクとして動作するジェネレータオブジェクトです。                    |
| name          | str, オプション | タスクに付ける名前の文字列です。省略時は適当な名前が自動的に生成されます。      |
| previous_task | `<etask>`, オプション | 指定された場合、このタスクは指定されたタスクの終了後に実行されます。      |
| start         | bool, オプション  | True（デフォルト）の場合、生成したタスクを即時開始します。False の場合は start() メソッドによる開始指示があるまで停止します。 |

- タスクとして動作させるジェネレータオブジェクト、またはそのソースコードを以下では「タスクジェネレータ」と呼びます。

<br>

### 1.4. 　start()　タスクを開始/再開する

開始指示待ちのタスク、または pause() で中断されたタスクを開始/再開します。

#### 書式： <!-- omit in toc -->

    <etask>.start()

<br>

### 1.5. 　pause()　タスクを中断する

タスクを中断します。

sync=True を指定すると、タスクを同期ポイントで中断します。sync=False（デフォルト）の場合は、その場で中断します。中断したタスクは start() メソッドで再開できます。

#### 書式： <!-- omit in toc -->

    <etask>.pause(sync=False)

<br>

### 1.6. 　stop()　タスクを終了する

タスクを終了します。

sync=True を指定すると、タスクを同期ポイントで終了します。sync=False（デフォルト）の場合は、その場で終了します。

#### 書式： <!-- omit in toc -->

    <etask>.stop(sync=False)

<br>

### 1.7. 　Suspender()　with構文を使ってturnの開始を一時的に停止させる（サブクラス）

イベントループを一時的に停止し（タスクの状態更新も一時的に停止します）、特定の処理を割り込ませるためのコンテキストマネージャーです。

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

---

## 2. 　class Button()　押しボタンの状態を取得するクラス

押しボタンの状態を監視し、あらかじめ設定された機能を実行するためのクラスです。<br>
（本クラスの機能はすべて、バックグラウンドタスクとして実行されます。）

### 2.1. 　start()　ボタン情報を取得するタスクを開始する

ボタン情報を定期的に取得するバックグラウンドタスクを開始するクラスメソッドです。

#### 書式： <!-- omit in toc -->

    <etask> = Button.start(pull_up=None, name="Bloop", tracelevel=0, period=0)

### 引数： <!-- omit in toc -->

| 名前       | 型         | 内容                                                                           |
| ---------- | ---------- | ------------------------------------------------------------------------------|
| pull_up    | Bool, オプション | ボタンが pull_up設定かどうかのデフォルトを設定します。省略時は初期設定、または前回の設定が維持されます。   |
| name       | str, オプション  | バックグラウンドタスクの名前を設定します。省略した場合、"Bloop" が設定されます。    |
| tracelevel | int, オプション  | トレース情報の出力レベルを設定します（デバッグ用）。省略した場合、0（出力しない）となります。 |
| period     | int, オプション  | ボタンの状態をポーリングする間隔をミリ秒単位で指定します。省略した場合、初期設定（100 ミリ秒）または前回の設定が維持されます。 |

- トレース情報出力レベルの詳細については [付録６ トレース情報出力レベル](#286-付録６トレース情報出力レベル) を参照してください。

<br>

### 2.2. 　str_reason()　状態コード(reason)に対応する状態文字列の取得

状態コード(reason)に対応する、状態を表す文字列を返すクラスメソッドです。

- 状態コードと状態を表す文字列の対応については、[付録３ 状態コード](#283-付録３状態コード) を参照してください。

#### 書式： <!-- omit in toc -->

    <str> = Button.str_reason(reason)

<br>

### 2.3. 　Button()　押しボタンを設定する（コンストラクタ）

指定された Pin、GPIO 番号、または Bootsel_button オブジェクトに対して、「押しボタン」オブジェクトを生成します。

#### 書式： <!-- omit in toc -->

    <button> = Button(pin, name="noname", pull_up=None,
                      hold_time=None, repeat_time=None,
                      on_action=None,
                      on_pressed=None,
                      on_released=None,
                      on_held=None)

#### 引数： <!-- omit in toc -->

| 名前        | 型                       | 内容                                                       |
| ----------- | ------------------------ | ---------------------------------------------------------- |
| pin         | Pin, int, Bootsel_button | 割り当てる Pin オブジェクト、GPIO 番号、または Bootsel_button オブジェクトを指定します。                            |
| name        | str, オプション       | ボタンの名前（任意）です。省略した場合、"noname" が設定されます。 |
| pull_up     | bool, オプション      | 押したときに Low になる場合は True を指定します。省略した場合、None（デフォルト設定）となります。 |
| hold_time   | float, オプション     | 長押し (HELD) および繰り返し (REPEATED) 開始までの遅延時間（秒）を設定します。 |
| repeat_time | float, オプション     | 繰り返し (REPEATED) の間隔（秒）を設定します。     |
| on_action   | function, オプション  | ボタンが操作された（押された、離された、長押しされた）ときに呼び出す関数を設定します。  |
| on_pressed  | function, オプション  | ボタンが押されたときに呼び出す関数を設定します。 |
| on_released | function, オプション  | ボタンが離されたときに呼び出す関数を設定します。     |
| on_held     | function, オプション  | ボタンが長押しされたときに呼び出す関数を設定します。   |

<br>

- ボタンが「繰り返し押された（REPEATED）」場合は、その回数分「押された」場合の関数が呼び出されます。
- hold_time、repeat_time の指定によるボタンのモードについては、[付録１ ボタンのモードの指定](#281-付録１ボタンのモードの指定) を参照してください。
- on_xxxx による関数の呼び出し契機については、[付録２ ファンクションの呼び出し契機](#282-付録２ファンクションの呼び出し契機) を参照してください。
- 引数 on_xxxx= による関数の設定は、メソッド on_xxxx() によるものと同じですが、ここでは関数の引数を同時に設定することができません。関数の引数まで設定する場合は各メソッドを使用するか、[Mu() Instant Closureクラス](#4-class-muinstant-closureクラス) を併用してください。

<br>

### 2.4. 　on_action()　ボタンが操作されたときに呼び出すファンクションを設定する

ボタンが操作された（押された、離された、長押しされた）際に呼び出される関数を設定します。

- ボタンが「繰り返し押された（REPEATED）」場合は、その回数分「押された」ものとして関数が呼び出されます。

#### 書式： <!-- omit in toc -->

    <button>.on_action(func, *args, myself=True, **kwargs)

### 引数一覧 <!-- omit in toc -->

| 名前     | 型             | 内容                                                 |
| -------- | -------------- | ---------------------------------------------------- |
| func     | function       | 呼び出す関数オブジェクトを指定します。           |
| *args    | 位置引数, オプション  | 関数に渡す位置引数を指定します。                       |
| myself   | bool, オプション  | True（デフォルト）の場合、呼び出す関数に Button オブジェクト自身を最初の引数として渡します。|
| **kwargs | キーワード引数, オプション | 関数に渡すキーワード引数を指定します。                  |

<br>

### 2.5. 　on_pressed()　ボタンが押されたときに呼び出すファンクションを設定する

- ボタンが押されたときに呼び出すファンクションを設定する

#### 書式 <!-- omit in toc -->

```python
<button>.on_pressed(func, *args, myself=None, **kwargs)
```

### 引数一覧 <!-- omit in toc -->

| 名前     | 型             | 内容                                                 |
| -------- | -------------- | ---------------------------------------------------- |
| func     | function       | 呼び出すファンクション                               |
| *args    | 位置引数       | ファンクションに渡す位置引数                         |
| myself   | bool, None     | Trueの場合、ファンクションに自身のインスタンスを渡す |
| **kwargs | キーワード引数 | ファンクションに渡すキーワード引数                   |

<br>

### 2.6. 　on_released()　ボタンが離されたときに呼び出すファンクションを設定する

- ボタンが離されたときに呼び出すファンクションを設定する

#### 書式 <!-- omit in toc -->

```python
<button>.on_released(func, *args, myself=None, **kwargs)
```

### 引数一覧 <!-- omit in toc -->

| 名前     | 型             | 内容                                                 |
| -------- | -------------- | ---------------------------------------------------- |
| func     | function       | 呼び出すファンクション                               |
| *args    | 位置引数       | ファンクションに渡す位置引数                         |
| myself   | bool, None     | Trueの場合、ファンクションに自身のインスタンスを渡す |
| **kwargs | キーワード引数 | ファンクションに渡すキーワード引数                   |

<br>

### 2.7. 　on_held()　ボタンが長押しされたときに呼び出すファンクションを設定する

- ボタンが長押しされたときに呼び出すファンクションを設定する

#### 書式 <!-- omit in toc -->

```python
<button>.on_held(self, func, *args, myself=None, **kwargs)
```

### 引数一覧 <!-- omit in toc -->

| 名前     | 型             | 内容                                                 |
| -------- | -------------- | ---------------------------------------------------- |
| func     | function       | 呼び出すファンクション                               |
| *args    | 位置引数       | ファンクションに渡す位置引数                         |
| myself   | bool, None     | Trueの場合、ファンクションに自身のインスタンスを渡す |
| **kwargs | キーワード引数 | ファンクションに渡すキーワード引数                   |

<br>
<br>

### 2.8. 付録

#### 2.8.1. 　付録１　ボタンのモードの指定

- ボタンのモードは、Button() による押しボタン定義時の hold_time、repeat_time 引数の指定による

| モード | held_time | repeat_time | 備考                                         |
| ------ | --------- | ----------- | -------------------------------------------- |
| 通常   | なし      | なし        |
| repeat | なし      | 指定あり    | repeat_timeで繰り返し                        |
| repeat | 指定あり  | 指定あり    | 初回はheld_time、以降はrepeat_timeで繰り返し |
| 長押し | 指定あり  | なし        | held_timeで長押し判定                        |

<br>

#### 2.8.2. 　付録２　ファンクションの呼び出し契機

- ボタンが操作されたときファンクションを呼び出す契機には、次の３種類のモードがある<br>
（on_actionで指定したファンクションは、すべての契機で呼び出される）

|     | モード | ファンクション呼び出し | 契機                                               |
| --- | ------ | ---------------------- | -------------------------------------------------- |
| 1   | 通常   | on_pressed             | ボタンが押されたとき                               |
|     |        | on_released            | ボタンが離されたとき                               |
| 2   | repeat | on_pressed             | ボタンが押されたとき                               |
|     |        | on_pressed             | ボタンが押され続けたとき（on_repeat は存在しない） |
|     |        | on_released            | ボタンが離されたとき                               |
| 3   | 長押し | on_pressed             | ボタンが押されたとき                               |
|     |        | on_held                | ボタンが長押し後、離されたとき                     |
|     |        | on_released            | ボタンが長押しされず、離されたとき                 |

<br>

#### 2.8.3. 　付録３　状態コード

| 状態コード | 状態を表す文字列 | 意味                     |
| ---------- | ---------------- | ------------------------ |
| 0          | "NONE"           | ボタンが操作されていない |
| 1          | "PRESSED"        | ボタンが押された         |
| 2          | "RELEASED"       | ボタンが離された         |
| 3          | "HELD"           | ボタンが長押しされた     |
| 4          | "REPEATED"       | ボタンが押し続けられた   |
| 5以上      | "unknown"        |                          |

<br>

#### 2.8.4. 　付録４　特別引数 myself

- on_xxxx で呼び出すファンクションのキーワード引数に myself=True を指定することにより、ファンクション側で以下の情報を取得できる
- myself=True を指定した場合、ファンクション側で必ず **「位置引数の１番目」** で myself引数を受け取る必要がある
- on_actionでは省略時 True、その他の on_xxxx では省略時 Falseになる

| 変数                 | 型           | 意味                                             |
| -------------------- | ------------ | ------------------------------------------------ |
| myself               | オブジェクト | functionを呼び出した Buttonオブジェクト          |
| myself.name          | str          | ボタンの名前                                     |
| myself.reason        | int          | functionが呼び出された理由（状態コード）         |
| myself.count         | int          | ボタンが押された回数（REPEATEDはカウントしない） |
| myself.repeat_count  | int          | repeat回数                                       |
| myself.interval_time | float        | 前回押された時から今回押されるまでの時間（秒）   |
| myself.inactive_time | float        | 前回解放から押されるまでの時間（秒）             |
| myself.active_time   | float        | 押されてから離されるまでの時間（秒）             |

- 状態コードは [付録３ 状態コード](#283-付録３状態コード) を参照

<br>

#### 2.8.5. 　付録５　Button情報の取得
- 以下の情報を外部から取得することができる

| 変数                  | 型   | 意味                       |
| --------------------- | ---- | -------------------------- |
| `<button>`.is_pressed | bool | ボタンが押されている状態か |

<br>

#### 2.8.6. 　付録６　トレース情報出力レベル
- Button.start() で指定する tracelevelに対応する出力内容
- tracelevelで指定した整数以下の情報が出力される<br>
（例えば、tracelevel=11 を指定すると、0 ～ 11までのトレース情報が出力される）

| tracelevel | 出力内容             | 発生タイミング             |
| ---------- | -------------------- | -------------------------- |
| 5          | ループ起動メッセージ | ボタン情報取得ループ起動時 |
| 10         | ボタン操作情報       | ボタン操作時               |
| 11         | ファンクション情報   | ボタン操作時               |
| 22         | ループ情報           | ボタン情報取得に行ったとき |

<br>
<br>

---

## 3. 　class Bootsel_button()　bootselボタンを他のPin入力と同様に扱うためのクラス

### 3.1. 　Bootsel_button()　bootselボタンを設定する（コンストラクタ）

#### 書式 <!-- omit in toc -->

```python
<bootsel_button> = Bootsel_button()
```

<br>

#### 使用例 <!-- omit in toc -->

```python
btn_0 = Button(Bootsel_button(), name="Bootsel_button", hold_time=1.0,
                on_released=led_0.flicker,
                on_held=led_0.off
                )
```

### 3.2. 　value()　bootsel_buttonの状態を返す

- bootsel_buttonが押されていたら 1、押されていなかったら 0 を返す

### 書式 <!-- omit in toc -->

```python
<int> = <bootsel_button>.value()
```

<br>
<br>

---

## 4. 　class Mu()　Instant Closureクラス

- 普通の関数(func)をクロージャーとして埋め込むクラスの MicroPythonバージョン
- Button() の引数としてファンクションを引き渡すときに、そのファンクションの引数も一緒に定義するときに使用する

### 4.1. 　Mu()　クロージャーを生成する

#### 書式 <!-- omit in toc -->

```python
<closure_func> = Mu(func, *args, **kwargs)
```

### 引数一覧 <!-- omit in toc -->

| 名前     | 型             | 内容                               |
| -------- | -------------- | ---------------------------------- |
| func     | function       | 埋め込むファンクション             |
| *args    | 位置引数       | ファンクションに渡す位置引数       |
| **kwargs | キーワード引数 | ファンクションに渡すキーワード引数 |

#### 使用例 <!-- omit in toc -->

```python
    btn_ledR = Button(6, name="Btn_ledR", hold_time=1.0,
                      on_released=Mu(ledR.blink, on_time=1.0, off_time=0.2),
                      on_held=ledR.stop_background
                      )
```

<br>
<br>

---

## 5. 　class LED()　LEDを制御するクラス

- LEDを制御するクラス（Signalのサブクラス）

### 5.1. 　LED()　LEDを設定する（コンストラクタ）

- LEDを接続したGPIO番号、または内蔵LEDに対して「LED」オブジェクトを作成するコンストラクタ

#### 書式 <!-- omit in toc -->

```python
<led> = LED(pno, value=0, invert=False)
```

#### 引数一覧 <!-- omit in toc -->

| 名前   | 型       | 内容                                                                                                                                           |
| ------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| pno    | int, str | GPIO番号、または "led"                                                                                                                         |
| value  | int      | LED初期値（消灯:0 または 点灯:1）                                                                                                              |
| invert | bool     | pinが highの時に LEDが点灯する場合（正論理）、invert=False (default)を、<br>pinが lowの時に LEDが点灯する場合（負論理）、invert=Trueを指定する |

<br>

### 5.2. 　on()　LEDを点灯する

- LEDを点灯する
- blink 等のバックグラウンド処理があれば先に停止する

#### 書式 <!-- omit in toc -->

```python
<led>.on(within=None)
```

### 5.3. 　on_for()　LEDを指定秒数点灯する

- LEDを点灯し、指定(seconds)秒数後に消灯する
- seconds が 0以下の場合は on() と同じ（点灯し消灯しない）
- blink 等のバックグラウンド処理があれば先に停止する

#### 書式 <!-- omit in toc -->

```python
<led>.on_for(seconds=0)
```

<br>

### 5.4. 　off()　LEDを消灯する

- LEDを消灯する
- blink 等のバックグラウンド処理があれば先に停止する

#### 書式 <!-- omit in toc -->

```python
<led>.off()
```

<br>

### 5.5. 　toggle()　LEDの点灯と消灯を切り替える

- LEDの現在の点灯／消灯を反転する

#### 書式 <!-- omit in toc -->

```python
<led>.toggle()
```

<br>

### 5.6. 　blink()　バックグラウンドで LEDを点滅させる

- バックグラウンドで LEDを点滅させる
- 他のバックグラウンド処理があれば先に停止する

#### 書式 <!-- omit in toc -->

```python
<etask> = <led>.blink(on_time=1.0, off_time=1.0, n=None, previous_task=None)
```

#### 引数一覧 <!-- omit in toc -->

| 名前          | 型              | 内容                                                                        |
| ------------- | --------------- | --------------------------------------------------------------------------- |
| on_time       | float           | 点灯時間（秒）                                                              |
| off_time      | float           | 消灯時間（秒）                                                              |
| n             | int, None       | 点滅回数。0 または Noneのときは永久に繰り返す                               |
| previous_task | `<etask>`, None | 指定された場合、先行する疑似スレッド（`<etask>`）の終了後に本処理を実行する |

<br>

### 5.7. 　flicker()　バックグラウンドで LEDを点滅させる（blinkと引数の指定方法が違うだけ）

- バックグラウンドで LEDを点滅させる（blinkと引数の指定方法が違うだけ）
- 他のバックグラウンド処理があれば先に停止する

#### 書式 <!-- omit in toc -->

```python
<etask> = <led>.flicker(interval=1.0, duty=0.5, n=None, previous_tasko=None)
```

#### 引数一覧 <!-- omit in toc -->

| 名前          | 型              | 内容                                                                        |
| ------------- | --------------- | --------------------------------------------------------------------------- |
| interval      | float           | 点滅間隔（秒）                                                              |
| duty          | float           | 点滅間隔に対する点灯時間の比率。0.5 で点灯時間=消灯時間になる               |
| n             | int, None       | 点滅回数。0 または Noneのときは永久に繰り返す                               |
| previous_task | `<etask>`, None | 指定された場合、先行する疑似スレッド（`<etask>`）の終了後に本処理を実行する |

<br>

### 5.8. 　y_blink()　LEDを点滅させるタスクジェネレータ

#### 書式 <!-- omit in toc -->

```python
<etask> = Edas(<led>.y_blink, on_time, off_time, n)
```

#### 引数一覧 <!-- omit in toc -->

| 名前     | 型         | 内容                                          |
| -------- | ---------- | --------------------------------------------- |
| on_time  | int, float | 点灯時間（秒）                                |
| off_time | int, float | 消灯時間（秒）                                |
| n        | int, None  | 点滅回数。0 または Noneのときは永久に繰り返す |

<br>

### 5.9. 　stop_background()　バックグラウンド処理を停止する

- blinkなどのバックグラウンド処理を停止する
- sync=True を指定すると、バックグラウンド処理を syncポイントまで実行した後停止する。False の場合は即停止する<br>（指定を省略すると True）

#### 書式 <!-- omit in toc -->

```python
<pwmled>.stop_background(sync=True)
```

<br>

### 5.10. 　stop_background_and_execute()　バックグラウンド処理を停止した後、指定処理を実行する

- blinkなどのバックグラウンド処理を停止した後 func を実行する
- sync=True を指定すると、バックグラウンド処理を syncポイントまで実行した後停止する。False の場合は即停止する<br>（指定を省略すると False）

#### 書式 <!-- omit in toc -->

```python
<pwmled>._after_background(func, sync=False)
```

<br>
<br>

---

## 6. 　class PWMLED()　LEDを PWMを用いて制御するクラス

- LEDを PWMを用いて制御するクラス（PWMのサブクラス）

### 6.1. 　PWMLED()　PWMLEDを設定する（コンストラクタ）

- LEDを接続したGPIO番号、Pin、またはLEDオブジェクトに対して「PWMLED」オブジェクトを作成するコンストラクタ

#### 書式 <!-- omit in toc -->

```python
<pwmled> = PWMLED(pin, freq=100, value=0.0, lo=0.0, hi=1.0, invert=False, curve=1.0)
```

#### 引数一覧 <!-- omit in toc -->

| 名前   | 型            | 内容                                                                                                                                            |
| ------ | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| pin    | int, LED, pin | 対象のpinを、pin番号(int)、 LED、 Pin などで指定する                                                                                            |
| freq   | int           | PWM出力の周波数(Hz)を指定する。省略時は 100Hzになる                                                                                             |
| value  | float         | PWM出力のduty比率の初期時を 0.0～1.0の値で指定する。省略時は 0.0になる                                                                          |
| lo     | float         | PWM出力のduty比率の最低値を設定する。省略時は 0.0になる                                                                                         |
| hi     | float         | PWM出力のduty比率の最高値を設定する。省略時は 1.0になる                                                                                         |
| invert | bool          | pinが highの時に LEDが点灯する場合（正論理）、invert=False (default)を、<br>pinが lowの時に LEDが点灯する場合（負論理）、invert=Trueを指定する  |
| curve  | float         | duty比率の指定値と物理値の対数カーブを指定する。1.0より大きい値を指定すると、duty比率に対する LEDの明るさが「緩やか」になる。省略値は 1.0になる |

- 対数カーブに指定する値
  - curve ＜ 1.0： 「Cカーブ」相当
  - curve=1.0： リニア（ 「Bカーブ」相当）
  - curve=1.5 ～ 2.5： volumeで言う「Aカーブ」相当
  - curve ＞ 2.5： 「Dカーブ」とかなんとか

<br>

### 6.2. 　on()　PWMLEDを点灯する（duty比を最高値にする）

- PWMLEDを点灯する（duty比を最高値にする）
- バックグラウンド処理があれば先に停止する

#### 書式 <!-- omit in toc -->

```python
<pwmled>.on()
```

### 6.3. 　off()　PWMLEDを消灯する（duty比を最低値にする）

- PWMLEDを消灯する（duty比を最低値にする）
- バックグラウンド処理があれば先に停止する

#### 書式 <!-- omit in toc -->

```python
<pwmled>.off()
```

<br>

### 6.4. 　toggle()　現在の duty比を逆転する

#### 書式 <!-- omit in toc -->

```python
<pwmled>.toggle()
```

<br>

### 6.5. 　duty()　PWMの duty比率を設定／取得する

- PWMの duty比率（value）を 0.0～1.0 の範囲で設定する。引数省略時は現在の duty比率を返す

#### 書式 <!-- omit in toc -->

```python
<float> = <pwmled>.duty(value=None)
```

<br>

### 6.6. 　value()　PWMの duty比率を設定／取得する（duty() と同じ）

- PWMの duty比率（value）を 0.0～1.0 の範囲で設定する。引数省略時は現在の duty比率を返す
- 機能は duty() と同一

#### 書式 <!-- omit in toc -->

```python
<float> = <pwmled>.value(value=None)
```

<br>

### 6.7. 　fadein()　PWMの duty比を、現在値から最高値まで連続して変化させる

- PWMの duty比を、現在値から最高値まで fade_time秒かけて変化させる
- 他のバックグラウンド処理があれば先に停止する

#### 書式 <!-- omit in toc -->

```python
<etask> = <pwmled>.fadein(fade_time=1.0)
```

<br>

### 6.8. 　fadeout()　PWMの duty比を現在値から最低値まで連続して変化させる

- PWMの duty比を、現在値から最低値まで fade_time秒かけて変化させる
- 他のバックグラウンド処理があれば先に停止する

#### 書式 <!-- omit in toc -->

```python
<etask> = <pwmled>.fadeout(fade_time=1.0)
```

<br>

### 6.9. 　_fade()　PWMの duty比を指定の開始 duty比から指定の終了 duty比まで連続して変化させる

- PWMの duty比を指定の開始 duty比から指定の終了 duty比まで fade_time秒かけて変化させる
- fadein()、fadeout() が呼び出している内部関数

#### 書式 <!-- omit in toc -->

```python
<etask> = <pwmled>._fade(fade_time, duty_from=0.0, duty_to=1.0)
```

<br>

### 6.10. 　y_fade()　fadein、fadeout するためのタスクジェネレータ

#### 書式 <!-- omit in toc -->

```python
<generator> = <pwmled>.y_fade(fade_time, duty_from, duty_to)
```

<br>

### 6.11. 　blink()　PWMLEDを点滅させる

- PWMLEDを、duty比率最低値～最高値の間で点滅させる
- 指定により、点灯時、点灯終了時に fadein/fadeoutを行う
- 他のバックグラウンド処理があれば先に停止する
- 

#### 書式 <!-- omit in toc -->

```python
<etask> = <pwmled>.blink(on_time=1.0, off_time=1.0, fade_in_time=0.0, fade_out_time=0.0, n=None)
```

#### 引数一覧 <!-- omit in toc -->

| 名前          | 型        | 内容                                                                           |
| ------------- | --------- | ------------------------------------------------------------------------------ |
| on_time       | float     | 点灯時間（秒）、省略時は 1.0秒                                                 |
| off_time      | float     | 消灯時間（秒）、省略時は 1.0秒                                                 |
| fade_in_time  | float     | 点灯時間中、duty比率を最低値から最高値まで変化させる時間（秒）、省略時は 0.0秒 |
| fade_out_time | float     | 点灯時間中、duty比率を最高値から最低値まで変化させる時間（秒）、省略時は 0.0秒 |
| n             | int, None | 点滅回数。0 または Noneのときは永久に繰り返す                                  |

<br>

### 6.12. 　y_blink()　PWMLED を点滅させるタスクジェネレータ

#### 書式 <!-- omit in toc -->

```python
<generator> = <pwmled>.y_blink(on_time, off_time, fade_in_time, fade_out_time, n)
```

<br>

### 6.13. 　pulse()　PWMLEDを連続して点滅させる

- PWMLEDを、duty比率最低値～最高値の間で連続して点滅させる
- 点滅時に fadein/fadeoutを行う
- 他のバックグラウンド処理があれば先に停止する

#### 書式 <!-- omit in toc -->

```python
<etask> = <pwmled>.pulse(fade_in_time=1.0, fade_out_time=1.0, n=None)
```

#### 引数一覧 <!-- omit in toc -->

| 名前          | 型        | 内容                                                               |
| ------------- | --------- | ------------------------------------------------------------------ |
| fade_in_time  | float     | duty比率を最低値から最高値まで変化させる時間（秒）、省略時は 0.0秒 |
| fade_out_time | float     | duty比率を最高値から最低値まで変化させる時間（秒）、省略時は 0.0秒 |
| n             | int, None | 点滅回数。0 または Noneのときは永久に繰り返す                      |

<br>

### 6.14. 　y_pulse()　PWMLEDを連続して点滅させるタスクジェネレータ

#### 書式 <!-- omit in toc -->

```python
<generator> = <pwmled>.y_pulse(fade_in_time, fade_out_time, n)
```

<br>

### 6.15. 　stop_background()　バックグラウンド処理を停止する

- blinkや fadeinなどのバックグラウンド処理を停止する
- sync=True を指定すると、バックグラウンド処理を syncポイントまで実行した後停止する。False の場合は即停止する<br>（指定を省略すると True）

#### 書式 <!-- omit in toc -->

```python
<pwmled>.stop_background(sync=True)
```

<br>

### 6.16. 　stop_background_and_execute()　バックグラウンド処理を停止した後、指定処理を実行する

- blinkや fadeinなどのバックグラウンド処理を停止した後 func を実行する
- sync=True を指定すると、バックグラウンド処理を syncポイントまで実行した後停止する。False の場合は即停止する<br>（指定を省略すると False）

#### 書式 <!-- omit in toc -->

```python
<pwmled>._after_background(func, sync=False)
```

<br>

