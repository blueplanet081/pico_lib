# Edas (並行処理モジュール)

## 概要
Edasは、MicroPythonのジェネレータ機能を使用して、シングルスレッドで並行処理を行うためのモジュールです。<br>
LEDを点滅させる、ボタンの状態を監視する、などの比較的低速な処理をバックグラウンドで行うのに適しています。<br>

Edasモジュールでは、コルーチン関数の記述にジェネレータ関数を用います。この関数、またはこの関数から生成したジェネレータオブジェクトを、本モジュールでは「タスクジェネレータ」と呼称します。
制御構造が単純な分、他のライブラリーやモジュール、自作関数などとの競合を回避しやすくなっています。

## 動作条件
以下は作成／テストで使用した環境です。<br>
Edasモジュールの本体は動作機種に（それほど？）依存しませんが、付録のクラスには一部機種依存する部分もあります。（機種依存部分の書き換えは多分簡単です）
- 動作環境: Raspberry Pi Pico W
- 言語: 
MicroPython v1.23.0 on 2024-06-02; Raspberry Pi Pico W with RP2040

## 何に使えるか

コルーチン関数は自由に記述して Edas上で並行処理を行うことができますが、
- LED（Pinに接続したledの点滅や時間制御）
- WPMLED（WPMを利用した明るさや点滅制御）
- Button（複数のボタンの監視と登録した処理の実行）

などのEdasを応用したモジュール（クラス）が付録についています。

## 特徴
- タイマーのチャンネルを一つだけ使用
- 通常の関数やメソッドを、内部の処理単位の間に「yield」文を挿入するだけで「疑似スレッド」化できる
- 各「疑似スレッド」の「処理単位（yield文で区切られた部分）」はタイマー割り込みに応じて順次実行されるので、疑似スレッド同士の競合が起きにくい
- としてジェネレータ関数を使用する以外、特殊な構造を持っていないため、（それなりに）見通しが良いプログラムになる
- そのため、スレッド（本物の）や他の非同期処理と競合しない
- 「疑似スレッド」の個々の処理は順次実行されるため、見掛け上非同期ながら同期的な動作も可能（複数の LEDをそれぞれ同期して点滅させる、とか）

## 構成


## class Edas():
    ''' 疑似スレッドクラス '''
    ここにクラスの説明を書く

##    class Freezed():
With構文を使って、疑似スレッドの状態更新を一時的に停止させる Edasクラス内のクラス

## with Edas.Freezed(freezetime=5)
with ブロック内に記述した文を実行する間、疑似スレッドの状態更新を一時的に停止する。

### freezetime
- 停止する単位時間を msec単位で指定する。
- ブロック内に記述した文の実行が freezetime内に終了しない場合は、単位時間を一区切りとして停止時間が延長される。
- デフォルトは 5 (msec)。


~~~py
    with Edas.Freezed():
        # ここに実例を入れる
~~~        

## Edas.__freeze_handler(freezetime):
疑似スレッドの状態更新を一時的に停止する内部クラスメソッド

freezetime
- 停止する単位時間を msec単位で指定する。
- 状態を解除するまでに単位時間を経過した場合は、単位時間を一区切りとして停止時間が延長される。
- 20 (msec)以上の値を指定した場合、20に切り下げられる。

## Edas.__defreeze_handler():
疑似スレッドの状態更新の一時的停止を解除する内部クラスメソッド




#### 疑似スレッドの状態
|状態(state) | 値       | 意味 |
|----------- |--------  |:----|
|NULL        |const(0)  |無効|
|START       |const(1)  |開始/再開（EXECに移行）|
|PAUSE       |const(2)  |停止|
|EXEC        |const(3)  |実行中
|S_PAUSE     |const(4)  |実行中で SYNC停止待ち
|S_END       |const(5)  |実行中で SYNC終了待ち
|END         |const(6)  |終了（deleteに移行）


#### 疑似スレッドのセッション実行結果
|実行結果    | 値       | 意味 |
|----------- |--------  |:----|
|SYNC        |const(22) |SYNCポイント
|IEND        |const(-1) |疑似スレッドのジェネレータが終了



## Edas(gen, followto=None, name=None, start=True)
疑似スレッドを生成するコンストラクタ

### gen
疑似スレッドの本体（ジェネレータ）。
### followto=None
先行する疑似スレッドを指定する。指定があれば、指定の疑似スレッドが終了後にこの疑似スレッドが実行される。省略時は指定なし(None)。
### name=None
疑似スレッドに付ける名前の文字列を指定する。省略時は、適当な名前が生成される。
### start=True
Trueを指定すると、疑似スレッドを生成後ただちに実行する。Falseを指定すると、実行待ちになる。省略時はTrue。


## Edas.ticks_ms()
ハンドラーの現在の turn の時刻(ms)を返すクラスメソッド。

## Edas.handler(timer):
定期的に起動されるハンドラー。タイマーループ内で自動実行される。

## Edas._set_follows(edas):
Edasの内部処理。

## Edas.start_loop(interval=None, tracelevel=None):
タイマーループを開始する。
### interval=None

    @classmethod
###    def stop_loop(cls):
        ''' タイマーループを停止する '''

    @classmethod
###    def show_edas(cls):
        ''' 疑似スレッドの一覧を表示する '''

    @classmethod
###    def stop_edas(cls, name=None, sync=False):
        ''' 疑似スレッドを停止する '''

    @classmethod
###    def _str_state(cls, state):
        ''' 疑似スレッドの状態を文字列で返す（デバッグ用） '''

    @classmethod
###    def __traceprint(cls, level, message, myself=None, previus_state=None, aftermessage=""):
        ''' デバッグ用プリント
            level 20～32 :もっと細かいトレース
            level 10～19 :状態変化出力
            level  ～ 9  :エラー出力
        '''            

###    def start(self):
        ''' 疑似スレッドを開始/再開する '''

###    def pause(self, sync=False):
        ''' 疑似スレッドを中断する '''

###    def stop(self, sync=False):
        ''' 疑似スレッドを終了する '''
