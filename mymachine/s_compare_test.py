from mymachine import s_compare

class PlainObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlotObject:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 組み込み型
print("int:", s_compare(5, 5))                  # True
print("str:", s_compare("abc", "abc"))          # True
print("list:", s_compare([1, 2], [1, 2]))        # True
print("tuple:", s_compare((1, 2), (1, 2)))       # True
print("dict:", s_compare({'a':1}, {'a':1}))      # True
print("nested dict:", s_compare(
    {'a': {'b': 2}}, {'a': {'b': 2}}))             # True

# 自作クラス（__dict__）
print("PlainObject (same):", s_compare(
    PlainObject(10, [1, 2]), PlainObject(10, [1, 2])))  # True
print("PlainObject (diff):", s_compare(
    PlainObject(10, [1, 2]), PlainObject(99, [1, 2])))  # False

# スロット使用クラス
print("SlotObject (same):", s_compare(
    SlotObject("hi", 5), SlotObject("hi", 5)))         # True
print("SlotObject (diff):", s_compare(
    SlotObject("hi", 5), SlotObject("hi", 8)))         # False

# 型が異なる
print("Different types:", s_compare([1, 2], (1, 2)))  # False

# __slots__ かつスロット未定義の属性
class PartialSlots:
    __slots__ = ('x',)
    def __init__(self):
        self.x = 42

a = PartialSlots()
b = PartialSlots()
b.x = 99
# a.x = 99
print("Slot diff attr:", s_compare(a, b))  # False