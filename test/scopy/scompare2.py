# MicroPythonで動作するコード
# 'import copy' は使用しない

# --- 比較対象の関数 ---
def scompare(obj1, obj2):
    """
    2つのオブジェクトの内容が浅いレベルで同一か調べる。
    MicroPythonでも動作する。
    """
    if type(obj1) is not type(obj2):
        return False

    if isinstance(obj1, (int, float, str, bool, type(None))):
        return obj1 == obj2

    try:
        vars1 = obj1.__dict__
        vars2 = obj2.__dict__
        return vars1 == vars2
        # return vars(obj1) == vars(obj2)
    except TypeError:
        return obj1 == obj2

# --- 動作確認用のクラス ---
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # MicroPythonでは __repr__ を定義するとREPLでの表示が分かりやすくなる
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# --- 実行と検証 ---

print("--- ケース1: 内容が同一なオブジェクト ---")
p1 = Point(10, 20)
p2 = Point(10, 20)
print(f"p1 = {p1}")
print(f"p2 = {p2}")
print(f"p1 is p2: {p1 is p2}")
print(f"scompare(p1, p2): {scompare(p1, p2)}")

print("\n--- ケース2: 内容が異なるオブジェクト ---")
p3 = Point(10, 99)
print(f"scompare(p1, p3): {scompare(p1, p3)}")

print("\n--- ケース3: __dict__を持たないオブジェクト（リスト） ---")
list1 = [1, 2, 3]
list2 = [1, 2, 3]
list3 = [4, 5, 6]
print(f"scompare(list1, list2): {scompare(list1, list2)}")
print(f"scompare(list1, list3): {scompare(list1, list3)}")