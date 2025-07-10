import time

import _thread
import time
from micropython import const

# class MyTimerStruct:
#     def __init__(self, owner, period, callback, mode):
#         self.owner = owner
#         self.period = period
#         self.callback = callback
#         self.mode = mode
#         self.next_trigger = time.ticks_add(time.ticks_ms(), period)

# class MyTimer:
#     PERIODIC = const(1)
#     ONE_SHOT = const(0)

#     _timers = {}
#     _running = False

#     def __init__(self, id):
#         self.id = id

#     def init(self, period, callback, mode=PERIODIC):
#         MyTimer._timers[self.id] = MyTimerStruct(owner=self, period=period, callback=callback, mode=mode)
#         if not MyTimer._running:
#             MyTimer._running = True
#             _thread.start_new_thread(MyTimer._run, ())

#     def deinit(self):
#         if self.id in MyTimer._timers:
#             del MyTimer._timers[self.id]

#     @staticmethod
#     def _run():
#         while True:
#             if not MyTimer._timers:
#                 MyTimer._running = False
#                 break

#             now = time.ticks_ms()
#             for id, t in list(MyTimer._timers.items()):
#                 if t.next_trigger > 0 and time.ticks_diff(now, t.next_trigger) >= 0:
#                     # ONE_SHOTは先にnext_triggerを0に（削除予定）
#                     if t.mode == MyTimer.ONE_SHOT:
#                         t.next_trigger = 0
#                     else:
#                         t.next_trigger = time.ticks_add(t.next_trigger, t.period)

#                     try:
#                         t.callback(t.owner)
#                     except Exception as e:
#                         print(f"[Timer {id}] callback error:", e)

#             # next_triggerが0のものは削除
#             for id in list(MyTimer._timers):
#                 if MyTimer._timers[id].next_trigger == 0:
#                     del MyTimer._timers[id]

#             time.sleep_ms(1)

from machine import Timer

if __name__ == '__main__':
    class Callbacks():
        def __init__(self, name="noname", mode=0, period=0):
            self.gcount = 0
            self.former_tm = time.ticks_ms()
            self.name = name
            self.mode = mode
            self.period = period

        def callback0(self, timer):
            ''' 順次実行形式 '''
            tm = time.ticks_ms()
            print()
            print(f"{self.gcount} [{self.name}] callback! {tm=} {time.ticks_diff(tm, self.former_tm)}")
            self.gcount += 1
            self.former_tm = tm

            # 遅延負荷
            j = 0
            for i in range(40000):
                j += i


            rt = time.ticks_diff(time.ticks_ms(), tm)
            print("Hoi!", f"{rt=} {self.period=}")
            timer.init(callback=self.callback0, period=(self.period - rt), mode=Timer.ONE_SHOT)

        def callback1(self, timer):
            ''' 定期実行形式 '''
            tm = time.ticks_ms()
            print(f"{self.gcount} [{self.name}] callback! {tm=} {time.ticks_diff(tm, self.former_tm)}")
            self.gcount += 1
            self.former_tm = tm

            # 遅延負荷
            j = 0
            for i in range(40000):
                j += i
            # time.sleep_ms(50)

    timer0 = Timer()     # MyTimer(0)
    timer1 = Timer()     # Mytimer(1)
    # timer = Timer(-1)       # machine.Timer

    cb0 = Callbacks(name="cb0", mode=Timer.ONE_SHOT, period=1000)     # 順次実行
    # cb0 = Callbacks(name="cb0")     # 順次実行
    cb1 = Callbacks(name="cb1")     # 定期実行
    # tmr = Callbacks(name="TMR")     # 定期実行（machine.Timer）

    # timer0.init(callback=cb0.callback0, period=1000, mode=MyTimer.ONE_SHOT)
    timer0.init(callback=cb0.callback0, period=1000, mode=Timer.ONE_SHOT)
    timer1.init(callback=cb1.callback1, period=800, mode=Timer.PERIODIC)
    # timer.init(callback=tmr.callback1, period=1000, mode=Timer.PERIODIC)


    try:
        for i in range(10):
            print(f"---- round {i} ----")
            print(f"{time.ticks_ms()=}")
            time.sleep(10)
    except KeyboardInterrupt:
        pass

    print("Normal End")