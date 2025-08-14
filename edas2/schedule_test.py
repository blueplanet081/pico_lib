# BUFFER_SIZE = 16
# buffer = [None] * BUFFER_SIZE
# write_index = 0
# read_index = 0

# def irq_handler(timer):
#     global buffer, write_index
#     value = read_sensor()  # 例：センサ値取得
#     next_index = (write_index + 1) % BUFFER_SIZE
#     if next_index != read_index:  # バッファが満杯でない
#         buffer[write_index] = value
#         write_index = next_index  # 書き込み位置更新

# def main_loop():
#     global buffer, read_index
#     while True:
#         if read_index != write_index:
#             value = buffer[read_index]
#             read_index = (read_index + 1) % BUFFER_SIZE
#             process(value)  # 例：LED制御やログ出力



# BUFFER_SIZE = 16
# buffer = [None] * BUFFER_SIZE
# write_index = 0
# read_index = 0
# count = 0  # 現在のバッファ内データ数

# def irq_handler(timer):
#     global buffer, write_index, count
#     if count < BUFFER_SIZE:
#         buffer[write_index] = read_sensor()
#         write_index = (write_index + 1) % BUFFER_SIZE
#         count += 1  # データ追加

# def main_loop():
#     global buffer, read_index, count
#     while True:
#         if count > 0:
#             value = buffer[read_index]
#             read_index = (read_index + 1) % BUFFER_SIZE
#             count -= 1  # データ消費
#             process(value)

class PulseBuffer:
    def __init__(self, size=16):
        self.size = size
        self.buffer = [None] * size
        self.write_index = 0
        self.read_index = 0
        self.count = 0

    def push(self, value) -> bool:
        if self.count < self.size:
            self.buffer[self.write_index] = value
            self.write_index = (self.write_index + 1) % self.size
            self.count += 1
            return True
        return False

    def pop(self):
        if self.count > 0:
            value = self.buffer[self.read_index]
            self.read_index = (self.read_index + 1) % self.size
            self.count -= 1
            return value
        return None

    def peek(self):
        if self.count > 0:
            return self.buffer[self.read_index]
        return None

    def is_full(self) -> bool:
        return self.count == self.size

    def is_empty(self) -> bool:
        return self.count == 0

    def clear(self):
        self.write_index = 0
        self.read_index = 0
        self.count = 0


class RPack():
    def __init__(self, buffer_size = 16) -> None:
        self.buffer_size = buffer_size
        self.buffer = [None] * self.buffer_size
        self.write_index = 0
        self.read_index = 0
        self.count = 0

    def write(self, value) -> bool:
        if self.count < self.buffer_size:
            self.buffer[self.write_index] = value
            self.write_index = (self.write_index + 1) % self.buffer_size
            self.count += 1
            return True
        return False

    def writable(self) -> bool:
        if self.count < self.buffer_size:
            return True
        return False

    def read(self):
        if self.count > 0:
            value = self.buffer[self.read_index]
            self.read_index = (self.read_index + 1) % self.buffer_size
            self.count -= 1
            return value
        else:
            return None

b1 = RPack(16)
for i in range(20):
    print(i)
    if b1.writable():
        b1.write(i)
    else:
        print("deny!!")

for i in range(20):
    value = b1.read()
    print(value)