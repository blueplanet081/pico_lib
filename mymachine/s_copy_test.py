from mymachine import s_copy, s_compare

class DictObj:
    def __init__(self):
        self.x = 10
        self.y = [1, 2]

class SlotObj:
    __slots__ = ('x', 'y')
    def __init__(self):
        self.x = "hi"
        self.y = (1, 2)

# 組み込み型
a = [1, 2, 3]
b = s_copy(a)
print("List copied:", b, b is not a)  # → True

d1 = {'a': 1, 'b': 2}
d2 = s_copy(d1)
print("Dict copied:", d2 == d1, d2 is not d1)  # → True

# 自作クラス（__dict__ベース）
o1 = DictObj()

print(dir(o1))
o2 = s_copy(o1)
print("DictObj copied:", o2.x == o1.x, o2.y == o1.y, o2 is not o1)  # → True
print(f"DictObj copied: {s_compare(o1, o2)=}")  # → True

# __slots__ ベースのクラス
s1 = SlotObj()
s2 = s_copy(s1)
print("SlotObj copied:", s2.x == s1.x, s2.y == s1.y, s2 is not s1)  # → True
print(f"SlotObj copied: {s_compare(s1, s2)=}")  # → True