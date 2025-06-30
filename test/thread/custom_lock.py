import _thread
import time

# --- 自作のシンプルなロッククラス ---
class MySimpleLock:
    def __init__(self):
        # 内部でMicroPythonの実際のロックを使用する
        # もしくは、ロック状態を管理するためのフラグと待機メカニズムを実装
        self._internal_lock = _thread.allocate_lock()
        print("MySimpleLock: ロックオブジェクトが初期化されました。")

    def __enter__(self):
        print("MySimpleLock: __enter__が呼び出されました。ロックを取得します...")
        self._internal_lock.acquire() # 実際のロックを取得
        print("MySimpleLock: ロックを取得しました。")
        return self # withブロック内でこのオブジェクト自体を使用できるようにする

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("MySimpleLock: __exit__が呼び出されました。ロックを解放します...")
        self._internal_lock.release() # 実際のロックを解放
        print("MySimpleLock: ロックを解放しました。")
        # 例外を抑制しない（withブロックの外に伝播させる）
        return False

# --- このカスタムロックを使用する例 ---

shared_resource = 0
custom_lock = MySimpleLock() # カスタムロックのインスタンスを作成

def thread_function():
    global shared_resource
    while True:
        # 自作のコンテキストマネージャーを使用
        with custom_lock:
            shared_resource += 1
            print(f"スレッド: shared_resourceを更新 -> {shared_resource}")
        time.sleep(0.5) # ロックを解放した後、少し待機

_thread.start_new_thread(thread_function, ())

while True:
    # メインプログラムも自作のコンテキストマネージャーを使用
    with custom_lock:
        print(f"メイン: shared_resourceを読み込み -> {shared_resource}")
    time.sleep(1.0) # ロックを解放した後、少し待機