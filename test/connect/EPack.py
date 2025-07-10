from mymachine import s_copy

class EPack:
    ''' mainプログラム、task間でデータを授受するクラス '''
    def __init__(self):
        self._contents = []
        self._work = None

    def send(self, value):
        ''' データを送信する '''
        if Edas.__in_task:
            self._contents.append(s_copy(value))
        else:
            Edas.__freezed = True
            self._contents.append(s_copy(value))
            Edas.__freezed = False

    def receive(self):
        ''' データを受信する '''
        if Edas.__in_task:
            if self._contents:
                return s_copy(self._contents.pop(0))
            return None
        else:
            Edas.__freezed = True
            if self._contents:
                self._work s_copy(self._contents.pop(0))
            else:
                self._work = None
            Edas.__freezed = False
            return self._work
