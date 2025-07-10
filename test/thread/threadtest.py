import machine
import time
import _thread


def core_id():
    return machine.mem32[0xd0000000]

class th_flag():
    def __init__(self):
        ''' スレッド制御用フラグ '''
        self.is_alive = False
        self.halt = False


def thread_test(thread_name: str):
    ledR = machine.Pin(16, machine.Pin.OUT)
    for _ in range(5):
        with lk:
            print(f'{thread_name=}')
            # cpuid = machine.mem32[0xd0000000]
            # print(f'{cpuid=}')
            print(f'{core_id()=}')
            for i in range(5):
                print(f'{thread_name} : {i}')
                ledR.on()
                time.sleep(0.3)
                ledR.off()
                time.sleep(0.5)


ledY = machine.Pin(17, machine.Pin.OUT)


lk = _thread.allocate_lock()

_thread.start_new_thread(thread_test, ('THREAD_1',))
# _thread.start_new_thread(thread_test, ('THREAD_2',))
time.sleep(1.5)

for _ in range(10):
    # with lk:
    #     cpuid = machine.mem32[0xd0000000]
    #     print(f'{cpuid=}')
    #     # print(f'{cpuid()=}')
    #     for i in range(5):
    #         print(f'main: {i}')
    #         time.sleep(0.2)
    # cpuid = machine.mem32[0xd0000000]
    # print(f'{cpuid=}')
    print(f'{core_id()=}')
    for i in range(5):
        print(f'main: {i}')
        ledY.on()
        time.sleep(0.1)
        ledY.off()
        time.sleep(0.2)
