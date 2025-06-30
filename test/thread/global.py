import _thread
import time

shared_data = 0
lock = _thread.allocate_lock() # 競合を避けるためのロック

def thread_function():
    global shared_data
    while True:
        with lock: # ロックを取得
            shared_data += 1
            print(f"Thread updated shared_data: {shared_data}")
        time.sleep(1)

_thread.start_new_thread(thread_function, ())

while True:
    with lock: # ロックを取得
        print(f"Main program read shared_data: {shared_data}")
    time.sleep(2)