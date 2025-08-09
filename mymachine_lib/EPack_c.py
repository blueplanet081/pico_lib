from mymachine_lib.mymachine2 import s_copy
import _thread

class EPack:
    STATUS_DEFAULT = 'DEFAULT'
    STATUS_PUSHER  = 'PUSHER'
    STATUS_POPPER  = 'POPPER'

    def __init__(self, status='DEFAULT', master=None):
        self._status = status
        self._lock = _thread.allocate_lock()
        self._contents = [] if status in ['DEFAULT', 'POPPER'] else None
        self._poppers = [] if status == 'DEFAULT' else None
        self._master = master  # PUSHER/POPPER 用

        if status == 'POPPER' and master:
            master.add_popper(self)

    def set_status(self, status, master=None):
        with self._lock:
            self._status = status
            if status in ['DEFAULT', 'POPPER']:
                self._contents = []
            else:
                self._contents = None
            if status == 'DEFAULT':
                self._poppers = []
            elif status in ['PUSHER', 'POPPER']:
                self._master = master
                if status == 'POPPER' and master:
                    master.add_popper(self)

    def push(self, value):
        if self._status == 'DEFAULT':
            val = s_copy(value)
            with self._lock:
                self._contents.append(val)
                for popper in self._poppers:
                    popper._receive(val)
        elif self._status == 'PUSHER' and self._master:
            self._master.push(value)
        else:
            raise Exception("Cannot push from current status")

    def pop(self):
        if self._status in ['DEFAULT', 'POPPER']:
            with self._lock:
                if self._contents:
                    return self._contents.pop(0)
                return None
        else:
            raise Exception("Cannot pop from current status")

    def _receive(self, value):
        '''マスターから受信する内部メソッド'''
        if self._status == 'POPPER':
            with self._lock:
                self._contents.append(s_copy(value))

    def add_popper(self, popper):
        if self._status == 'DEFAULT':
            self._poppers.append(popper)