<a id="document_top"></a>

# e_module モジュール説明書　 <!-- omit in toc -->

Raspberry Pi Pico W / Pico2 W 上でシングルスレッドのマルチタスクを実現するための基本モジュールです。

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

| ファイル名  | ver.   | 日付       | 内容                 |
| ----------- | ------ | ---------- | -------------------- |
| e_module.py | 作成中 | 2025/05/02 | モジュール本体       |
| e_module.md | 作成中 | 2025/05/02 | ドキュメント（本書） |

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

[ドキュメント先頭に戻る](#document_top)

<a id="method_list"></a>
## メソッド一覧 <!-- omit in toc -->

- [1. 　class Edas()](#1-class-edas)
  - [1.1. 　loop\_start()　イベントループを開始する（クラスメソッド）](#11-loop_startイベントループを開始するクラスメソッド)
  - [1.2. 　loop\_stop()　イベントループを停止する（クラスメソッド）](#12-loop_stopイベントループを停止するクラスメソッド)
  - [1.3. 　Freezed()　イベントループを一時的に停止する（内部クラス）](#13-freezedイベントループを一時的に停止する内部クラス)
  - [1.4. 　Edas()　タスクを生成する（コンストラクタ）](#14-edasタスクを生成するコンストラクタ)
  - [1.5. 　resume()　タスクを再開する](#15-resumeタスクを再開する)
  - [1.6. 　pause()　タスクを中断する](#16-pauseタスクを中断する)
  - [1.7. 　cancel() タスクを終了する](#17-cancel-タスクを終了する)
  - [1.8. 　done() タスクの終了を判定する](#18-done-タスクの終了を判定する)
  - [1.9. 　result() タスクの実行結果を返す](#19-result-タスクの実行結果を返す)
  - [1.10. 　cancel\_tasks() 　動作中の指定の性質のタスクを終了する（クラスメソッド）](#110-cancel_tasks-動作中の指定の性質のタスクを終了するクラスメソッド)
  - [1.11. 　cancel\_basic\_tasks() 　動作中の全ての通常タスクを終了する（クラスメソッド）](#111-cancel_basic_tasks-動作中の全ての通常タスクを終了するクラスメソッド)
  - [1.12. 　wait\_for\_idle() 　動作中の全ての通常タスクの終了を待つ（クラスメソッド）](#112-wait_for_idle-動作中の全ての通常タスクの終了を待つクラスメソッド)
  - [1.13. 　idle\_time() 　通常のタスクが動いていない時間を取得する（クラスメソッド）](#113-idle_time-通常のタスクが動いていない時間を取得するクラスメソッド)
  - [1.14. 　\_get\_taskcount() 　動いているタスクの本数を返す（クラスメソッド）](#114-_get_taskcount-動いているタスクの本数を返すクラスメソッド)
  - [1.15. 　ticks\_ms() 　イベントループの現在の turn 時刻(ミリ秒)を取得する（クラスメソッド）](#115-ticks_ms-イベントループの現在の-turn-時刻ミリ秒を取得するクラスメソッド)
  - [1.16. 　after()　指定時間（秒）後に functionを実行する（クラスメソッド）](#116-after指定時間秒後に-functionを実行するクラスメソッド)
  - [1.17. 　after\_ms()　指定時間（ミリ秒）後に functionを実行する（スタティックメソッド）](#117-after_ms指定時間ミリ秒後に-functionを実行するスタティックメソッド)
  - [1.18. 　y\_oneshot()　指定の関数を一回だけ実行するタスクジェネレータ（スタティックメソッド）](#118-y_oneshot指定の関数を一回だけ実行するタスクジェネレータスタティックメソッド)
  - [1.19. 　y\_sleep()　second秒が経過するまで yieldを繰り返すタスクジェネレータ（スタティックメソッド）](#119-y_sleepsecond秒が経過するまで-yieldを繰り返すタスクジェネレータスタティックメソッド)
  - [1.20. 　y\_sleep\_ms()　ms ミリ秒が経過するまで yieldを繰り返すタスクジェネレータ（スタティックメソッド）](#120-y_sleep_msms-ミリ秒が経過するまで-yieldを繰り返すタスクジェネレータスタティックメソッド)
  - [1.21. 　show\_edas()　動作中のタスクの一覧を表示するユーティリティメソッド（クラスメソッド）](#121-show_edas動作中のタスクの一覧を表示するユーティリティメソッドクラスメソッド)
  - [1.22. 　stop\_edas()　動作中のタスクを終了するユーティリティメソッド（クラスメソッド）](#122-stop_edas動作中のタスクを終了するユーティリティメソッドクラスメソッド)
  - [1.23. 　付録](#123-付録)
    - [1.23.1. 　付録１　トレース情報出力レベル](#1231-付録１トレース情報出力レベル)
    - [1.23.2. 　付録２　タスクの状態](#1232-付録２タスクの状態)
    - [1.23.3. 　付録３　タスクの性質](#1233-付録３タスクの性質)
- [2. 　CheckTime()　経過時間を管理するクラス](#2-checktime経過時間を管理するクラス)
  - [2.1. 　CheckTime()　コンストラクタ](#21-checktimeコンストラクタ)
  - [2.2. 　set()　基準時刻を trun時刻、または指定時刻に変更する](#22-set基準時刻を-trun時刻または指定時刻に変更する)
  - [2.3. 　add\_ms()　基準時刻を加算する](#23-add_ms基準時刻を加算する)
  - [2.4. 　ref\_time()　基準時刻を返す](#24-ref_time基準時刻を返す)
  - [2.5. 　y\_wait\_ms()　指定時間が経過するまで yieldを繰り返すタスクジェネレータ](#25-y_wait_ms指定時間が経過するまで-yieldを繰り返すタスクジェネレータ)

<br>
<br>

[ドキュメント先頭に戻る](#document_top)

## 1. 　class Edas()

シングルスレッドでマルチタスク処理を行うためのイベントループとタスク管理機能を提供するクラスです。

### 1.1. 　loop_start()　イベントループを開始する（クラスメソッド）

イベントループを開始するクラスメソッドです。

#### 書式： <!-- omit in toc -->

    Edas.loop_start(period=None, tracelevel=0)

#### 引数： <!-- omit in toc -->

| 名前       | 型  | 内容                                                                                         |
| ---------- | --- | -------------------------------------------------------------------------------------------- |
| period     | int | タイマーループの間隔をミリ秒単位で指定します。省略時は規定値、または現在の値が使用されます。 |
| tracelevel | int | トレース情報出力レベル（デバッグ用）を指定します。省略時は 0（出力しない）です。             |

- トレース情報出力レベルは [付録１ トレース情報出力レベル](e_module.md#appendix01)を参照してください。

<br>

### 1.2. 　loop_stop()　イベントループを停止する（クラスメソッド）

イベントループを停止するクラスメソッドです。

#### 書式： <!-- omit in toc -->

    Edas.loop_stop()

<br>

### 1.3. 　Freezed()　イベントループを一時的に停止する（内部クラス）

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

    <etask> = Edas(gen, name=None, ps=None, previous_task=None, pause=False, terminate_by_sync=False, task_nature=BASIC):

#### 戻り値： <!-- omit in toc -->

生成されたタスクオブジェクト（`<etask>`）を返します。

#### 引数： <!-- omit in toc -->

| 名前              | 型           | 内容                           |
| ----------------- | ------------ | ------------------------------------------------- |
| gen               | ジェネレータ | タスクとして動作するジェネレータオブジェクトです。      |
| name              | str          | タスクに付ける名前の文字列です。省略時は適当な名前が自動的に生成されます。      |
| previous_task     | `<etask>`    | 指定された場合、このタスクは指定されたタスクの終了後に実行されます。            |
| pause             | bool         | False（デフォルト）の場合、生成したタスクを即時開始します。True の場合は resume() メソッドによる開始指示があるまで停止します。 |
| on_cancel         | callable    | タスクがキャンセルされた時に実行する短い処理を指定します。省略時はタスクキャンセル時に何も実行しません。|
| terminate_by_sync | bool         | Truneの場合、タスクの終了時に 'SYNC'を待ちます。False（デフォルト）の場合は即時終了します。 |
| task_nature       | int          | タスクの性質を指定します。省略時は BASIC（通常のタスク）になります。            |

- タスクとして動作させるジェネレータオブジェクト、またはそのソースコードを以下では「タスクジェネレータ」と呼びます。
- 「タスクの性質」の指定方法と意味は [付録３ タスクの性質](e_module.md#appendix03) を参照してください。

<br>

### 1.5. 　resume()　タスクを再開する

開始指示待ちのタスク、または pause() で中断されたタスクを開始/再開します。

#### 書式：  <!-- omit in toc -->

    <etask>.resume()

<br>

### 1.6. 　pause()　タスクを中断する

タスクを中断します。

sync=True（デフォルト）を指定すると、同期ポイントがあるタスクは同期ポイントまで実行して中断します。<br>
sync=False を指定すると、タスクは即時に中断します。<br>
（同期ポイントが無いタスクは、syncの指定にかかわらず即時に中断します。）

#### 書式： <!-- omit in toc -->

    <etask>.pause(sync=True)

<br>

### 1.7. 　cancel() タスクを終了する

タスクを終了します。

- sync=True（デフォルト）を指定すると、同期ポイントがあるタスクは同期ポイントまで実行して終了します。<br>
sync=False を指定すると、タスクは即時に終了します。<br>
（同期ポイントが無いタスクは、syncの指定にかかわらず即時に終了します。）

#### 書式： <!-- omit in toc -->

    <etask>.cancel(sync=True)

<br>

### 1.8. 　done() タスクの終了を判定する

タスクが終了しているかどうかを判定します。<br>
タスクが終了していたら True、それ以外は Falseを返します。

#### 書式： <!-- omit in toc -->

    <bool> = <etask>.done()

<br>

### 1.9. 　result() タスクの実行結果を返す

タスクの実行結果（戻り値）を返します。<br>
タスクが終了していない、またはタスクに戻り値が無い場合は、Noneを返します。

#### 書式： <!-- omit in toc -->

    <return_value> = <etask>.result()

<br>

### 1.10. 　cancel_tasks() 　動作中の指定の性質のタスクを終了する（クラスメソッド）

動作中の指定の性質のタスクを終了するクラスメソッドです。

- sync=Trueを指定すると、同期ポイントがあるタスクは同期ポイントまで実行して終了します。<br>
sync=False（デフォルト） を指定すると、タスクは即時に終了します。<br>
（同期ポイントが無いタスクは、syncの指定にかかわらず即時に終了します。）
- 終了するタスクの「性質」は、配列で指定します。デフォルトは [Edas.BASIC, Edas.ANCILLARY]です。
- 「BASIC」、「ANCILLARY」およびそれ以外のタスクの性質については、[付録３ タスクの性質](e_module.md#appendix03) を参照してください。

#### 書式： <!-- omit in toc -->

    Edas.cancel_tasks(natures=[Edas.BASIC, Edas.ANCILLARY], sync=False)

<br>

### 1.11. 　cancel_basic_tasks() 　動作中の全ての通常タスクを終了する（クラスメソッド）

動作中の全ての通常タスク（task_nature=BASIC）を終了するクラスメソッドです。

- sync=Trueを指定すると、同期ポイントがあるタスクは同期ポイントまで実行して終了します。<br>
sync=False（デフォルト） を指定すると、タスクは即時に終了します。<br>
（同期ポイントが無いタスクは、syncの指定にかかわらず即時に終了します。）
- 「BASIC」などのタスクの性質については、[付録３ タスクの性質](e_module.md#appendix03) を参照してください。

#### 書式： <!-- omit in toc -->

    Edas.cancel_basic_tasks(sync=False)

<br>

### 1.12. 　wait_for_idle() 　動作中の全ての通常タスクの終了を待つ（クラスメソッド）

動作中の全ての通常タスク（task_nature=BASIC）の終了を待つクラスメソッドです。

- timeout が指定された場合、timeoutで指定した秒数まで終了しなかった場合は、それ以上待つことなくメソッドが終了します。timeoutが省略された場合はタイムアウトせず終了を待ちます。
- 「BASIC」などのタスクの性質については、[付録３ タスクの性質](e_module.md#appendix03) を参照してください。

#### 書式： <!-- omit in toc -->

    Edas.wait_for_idle(timeout=None)

<br>

### 1.13. 　idle_time() 　通常のタスクが動いていない時間を取得する（クラスメソッド）

イベントループ内で通常のタスク（task_nature=BASIC）が動作していない時間（秒）を取得するクラスメソッドです。

- 「BASIC」などのタスクの性質については、[付録３ タスクの性質](e_module.md#appendix03) を参照してください。

#### 書式： <!-- omit in toc -->

    <float> = Edas.idle_time()

<br>

### 1.14. 　_get_taskcount() 　動いているタスクの本数を返す（クラスメソッド）

イベントループの直前のターンで動いたタスクの本数を返します。

引数の natureは、カウントするタスクの性質を指定します。省略すると、全てのタスクの本数を返します。

#### 書式： <!-- omit in toc -->

    <int> = Edas._get_taskcount(nature=None)

<br>

### 1.15. 　ticks_ms() 　イベントループの現在の turn 時刻(ミリ秒)を取得する（クラスメソッド）

イベントループの現在のターン開始時刻（ミリ秒）を取得するクラスメソッドです。

複数のタスク間で、同一ターンの同期を取る場合に使用します。

#### 書式： <!-- omit in toc -->

    <turn時刻> = Edas.ticks_ms()

<br>

### 1.16. 　after()　指定時間（秒）後に functionを実行する（クラスメソッド）

バックグラウンドで動作し、指定時間 (delay: float, 秒) 経過後に function を実行します。

作成したタスクオブジェクト (`<etask>`) を返します。

#### 書式： <!-- omit in toc -->

    <etask> = Edas.after(delay, function)

<br>

### 1.17. 　after_ms()　指定時間（ミリ秒）後に functionを実行する（スタティックメソッド）

動作は after() と同じですが、指定時間を秒ではなくミリ秒 (delay_ms: int) で指定します。

#### 書式： <!-- omit in toc -->

    <etask> = Edas.after_ms(delay_ms, function)

<br>


### 1.18. 　y_oneshot()　指定の関数を一回だけ実行するタスクジェネレータ（スタティックメソッド）

指定の関数（func）を一回だけ実行して終了するタスクジェネレータです。


#### 書式： <!-- omit in toc -->

    <generator> = Edas.y_oneshot(func)


#### 使用例： <!-- omit in toc -->

- 動作中のタスク（self._background）を終了させ、終了後に指定関数（func）を実行させる例です。

```python
    def stop_background_and_execute(self, func, sync=False):
        ''' blink などのバックグラウンド処理を停止した後 func を実行する '''
        if self._background:
            ret = Edas(Edas.y_oneshot(func), previous_task=self._background)
            self._background.stop(sync)
        else:
            ret = func()
        return ret

```

<br>

### 1.19. 　y_sleep()　second秒が経過するまで yieldを繰り返すタスクジェネレータ（スタティックメソッド）

タスクジェネレータ内で、指定した時間 (second: 秒) が経過するまで yield を繰り返します。

#### 書式： <!-- omit in toc -->

    yield from Edas.y_sleep(second)

<br>

### 1.20. 　y_sleep_ms()　ms ミリ秒が経過するまで yieldを繰り返すタスクジェネレータ（スタティックメソッド）

タスクジェネレータ内で、指定した時間 (ms: ミリ秒) が経過するまで yield を繰り返します。

#### 書式： <!-- omit in toc -->

    yield from Edas.y_sleep_ms(ms)

<br>

### 1.21. 　show_edas()　動作中のタスクの一覧を表示するユーティリティメソッド（クラスメソッド）

現在動作しているタスクの一覧を vREPL上に表示するユーティリティメソッドです。

#### 書式（使い方）： <!-- omit in toc -->

    >>> from e_machine import Edas
    >>> Edas.show_edas()

<br>

### 1.22. 　stop_edas()　動作中のタスクを終了するユーティリティメソッド（クラスメソッド）

現在動作しているタスクを終了するユーティリティメソッドです。

name に終了するタスクの名前を指定します。省略時はすべてのタスクを終了します。<br>
sync=True を指定した場合、同期ポイントを持つタスクは同期ポイントまで実行した後に終了します。

#### 書式（使い方）： <!-- omit in toc -->

    >>> from mymachine import Edas
    >>> Edas.stop_edas(name=None, sync=False)

<br>

### 1.23. 　付録

<a id="appendix01"></a>
#### 1.23.1. 　付録１　トレース情報出力レベル

 [Edas.loop_start()](#11-loop_startイベントループを開始するクラスメソッド) で指定する tracelevel に対応する出力内容です。指定した整数以下のレベルの情報が出力されます。<br>
 （例えば、tracelevel=15 を指定すると、0 ～ 15までのトレース情報が出力されます。）

| tracelevel | 出力内容                 | 発生タイミング            |
| ---------- | ------------------------ | ------------------------- |
| 0          | メッセージ               | 随時                      |
| 8          | エラー等                 | エラー発生時              |
| 11         | タスク生成               | Edas()処理時              |
| 11         | フリーズ処理             | with Edas.Freezed()処理時 |
| 14         | タスクの状態             | タスクの状態変更時        |
| 15         | SYNC終了                 | タスクのSYNC終了検出時    |
| 18         | SYNC検出                 | タスクのSYNC検出時        |
| 22         | turnタスク実行処理開始   | turn                      |
| 24         | turn整列処理開始         | turn                      |
| 28         | turn開始時間、終了時間等 | turn                      |
| 32         | 個々のタスクの開始情報   | turn中の各タスク開始時    |

<br>

<a id="appendix02"></a>
#### 1.23.2. 　付録２　タスクの状態

システム内部で管理しているタスクの状態です。

| 状態    | 内部コード | 意味                        |
| ------- | ---------- | --------------------------- |
| NULL    | const(0)   | 無効                        |
| START   | const(1)   | 開始/再開（EXECに移行する） |
| PAUSE   | const(2)   | 停止                        |
| EXEC    | const(3)   | 実行中                      |
| S_PAUSE | const(4)   | 実行中で SYNC停止待ち       |
| S_END   | const(5)   | 実行中で SYNC終了待ち       |
| END     | const(6)   | 終了（DONEに移行する）      |
| DONE    | const(9)   | 終了                        |


<br>

<a id="appendix03"></a>
#### 1.23.3. 　付録３　タスクの性質

動作するタスクの「性質」です。

| 性質       | 内部コード | 意味                                |
| ---------- | ---------- | ----------------------------------- |
| CORE       | const(0)   | システム制御用（reserved）          |
| PERSISTENT | const(1)   | 継続的なタスク                      |
| BASIC      | const(2)   | 通常タスク                          |
| ANCILLARY  | const(3)   | いつ終了させても問題ないタスク      |
| UNKNOWN    | const(4)   | 管理対象外                          |

- PERSISTENT（継続的なタスク）は、e_machineモジュールの Bottonのように常時動作しているタスクに使われます。
- BASIC（通常のタスク）は、タスクの稼働状況の判断に使われます。BASICのタスクが１本も実行中でないときに、システムが空転中（idle）であると判断します。（その他の「性質」は空転中の判断に影響しません）
- 外部のプログラムから関数の引数として指定するときは、本モジュールから「Edas」を importして、「`Edas.BASIC`」のような形式で指定します。

<br>
<br>

[メソッド一覧に戻る](#method_list)

---

## 2. 　CheckTime()　経過時間を管理するクラス

基準時刻からの経過時間（ミリ秒）を管理するためのクラスです。

### 2.1. 　CheckTime()　コンストラクタ

CheckTime オブジェクトを生成し、基準時刻を現在の turn 時刻（ミリ秒）に設定します。

- 注： turn 時刻は Edas のタイマーループにおける各ターンの開始時刻であり、Edas.ticks_ms() で取得できます。

### 書式： <!-- omit in toc -->

    <ctime> = CheckTime()

<br>

### 2.2. 　set()　基準時刻を trun時刻、または指定時刻に変更する

基準時刻を turn 時刻、または指定した時刻（ミリ秒）に変更します。

- ms 引数にミリ秒単位の時刻を指定します。省略した場合、基準時刻は現在の turn 時刻に設定されます。
- 変更後の基準時刻（ミリ秒）を返します。

#### 書式： <!-- omit in toc -->

    <time_ms> = <ctime>.set(ms=None)

 <br>

### 2.3. 　add_ms()　基準時刻を加算する

基準時刻に delta（ミリ秒）を加算します。

- 変更後の基準時刻（ミリ秒）を返します。

#### 書式： <!-- omit in toc -->

    <time_ms> = <ctime>.add_ms(delta)

<br>

### 2.4. 　ref_time()　基準時刻を返す

現在の基準時刻(ミリ秒)を返します。

#### 書式： <!-- omit in toc -->

    <time_ms> = <ctime>.ref_time()

<br>

### 2.5. 　y_wait_ms()　指定時間が経過するまで yieldを繰り返すタスクジェネレータ

タスクジェネレータ内で、指定した時間 (wait_ms: ミリ秒) が経過するまで yield を繰り返します。

update=Trueを指定すると、時間経過後に基準時刻を wait_ms分だけ更新（加算）します。update=Falseの場合は、基準時刻を更新しません。

#### 書式： <!-- omit in toc -->

    yield from <ctime>.y_wait_ms(wait_ms, update=False)

#### 使用例： <!-- omit in toc -->

- タスクジェネレータ（lblink）内で、ledの点灯時間、消灯時間の調整に y_wait_ms() を使用する例です。

```python
from machine import Pin
from e_module import Edas, CheckTime

def lblink(pin, on_time, off_time, n):
    ctime = CheckTime()
    count = 0
    while not n or count < n:
        pin.value(1)
        yield from ctime.y_wait_ms(on_time, update=True)
        pin.value(0)
        yield from ctime.y_wait(off_time_ms, update=True)
        count += 1

led = Pin("LED", Pin.OUT)
Edas.loop_start()
Edas(lblink(led, 1000, 500, 5))

Edas.wait_for_idle()
```

<br>

[メソッド一覧に戻る](#method_list)
