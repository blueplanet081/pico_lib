import math

class HistoryBuffer:
    ''' 数値フィルター用リングバッファ '''
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.index = 0
        self.count = 0

    def add(self, value):
        ''' データを１件格納する '''
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size
        if self.count < self.size:
            self.count += 1

    def get(self):
        ''' バッファ内容をリストで取得する '''
        return [self.buffer[(self.index - i - 1) % self.size] for i in range(self.count)]

class NumericFilter:
    ''' 数値フィルターのベースクラス '''
    def __init__(self, history_size):
        self.history = HistoryBuffer(history_size)

    def is_numeric(self, value):
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    def apply(self, value):
        if not self.is_numeric(value):
            return value  # 数値でない場合はそのまま通す
        return self.apply_numeric(value)

    def apply_numeric(self, value):
        raise NotImplementedError("Subclasses must implement apply_numeric()")

class OutFilter(NumericFilter):
    ''' 外れ値フィルター '''
    def __init__(self, history_size, threshold):
        super().__init__(history_size)
        self.threshold = threshold

    def apply_numeric(self, value):
        values = self.history.get()
        if not values:
            self.history.add(value)
            return value
        avg = sum(values) / len(values)
        if abs(value - avg) > self.threshold:
            return None  # 外れ値として棄却
        self.history.add(value)
        return value
    
class MovAvgFilter(NumericFilter):
    ''' 移動平均値フィルター '''
    def apply_numeric(self, value):
        self.history.add(value)
        values = self.history.get()
        return sum(values) / len(values)

class MedFilter(NumericFilter):
    ''' 中央値フィルター '''
    def apply_numeric(self, value):
        self.history.add(value)
        values = self.history.get()
        sorted_values = sorted(values)
        n = len(sorted_values)
        if n % 2 == 1:
            return sorted_values[n // 2]
        else:
            return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2

