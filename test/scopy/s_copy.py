def s_copy(obj):
    """
    MicroPython向けの簡易的な shallow copy 実装。
    標準の copy.copy() の機能の一部を模倣します。
    """
    # 組み込みのミュータブルコンテナの特殊処理
    if isinstance(obj, list):
        return obj[:]
    elif isinstance(obj, dict):
        return obj.copy()
    elif isinstance(obj, set):
        return obj.copy()

    # イミュータブルだけど新しい objを作成
    elif isinstance(obj, tuple):
        return tuple(obj)

    # イミュータブルコンテナ
    elif isinstance(obj, (int, float, str, bool, type(None))):
        return obj

    # 以降、クラスのインスタンスのコピー処理

    # __copy__ メソッドが定義されていればそれを使用
    if hasattr(obj, '__copy__'):
        return obj.__copy__()

    # 新しい空のインスタンスを作成
    # __init__ を呼び出さない object.__new__ を使用するのが安全
    new_obj = object.__new__(obj.__class__)

    # インスタンスの属性をコピーする
    # __dict__ を持つクラスの場合
    if hasattr(obj, '__dict__'):
        for attr_name, attr_value in obj.__dict__.items():
            # object.__setattr__ を使うことで、カスタムの __setattr__ をバイパスできます。
            object.__setattr__(new_obj, attr_name, attr_value)

    # __slots__ のみで __dict__ を持たないクラスの場合
    elif hasattr(obj.__class__, '__slots__'):
        for attr_name in obj.__class__.__slots__:
            # スロットに定義されている属性のみをコピー
            # 元オブジェクトがそのスロット属性を持っているか確認 (設定されていない場合もあるため)
            if hasattr(obj, attr_name):
                attr_value = getattr(obj, attr_name)
                object.__setattr__(new_obj, attr_name, attr_value)

    else:
        print("Warning: Neither __dict__ nor __slots__ found for instance variables. "
              "Automatic attribute copying might be incomplete or incorrect.")

    return new_obj


# --- テスト用クラス ---
class MyDictClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __repr__(self):
        return f"MyDictClass(a={self.a}, b={self.b})"

class MySlottedClass:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"MySlottedClass(x={self.x}, y={self.y})"

class MyHybridSlottedClass: # __slots__ に __dict__ を含める稀なケース
    __slots__ = ('x', '__dict__')
    def __init__(self, x, z):
        self.x = x
        self.z = z # これは __dict__ に入る

# --- 動作確認 ---
if __name__ == '__main__':
    print("--- Testing MyDictClass ---")
    orig_dict_obj = MyDictClass(1, 2)
    copied_dict_obj = s_copy(orig_dict_obj)
    print(f"Original: {orig_dict_obj}")
    print(f"Copied:   {copied_dict_obj}")
    print(f"a from copied: {copied_dict_obj.a}") # 期待通りにアクセスできる

    print("\n--- Testing MySlottedClass ---")
    orig_slotted_obj = MySlottedClass(10, 20)
    copied_slotted_obj = s_copy(orig_slotted_obj)
    print(f"Original: {orig_slotted_obj}")
    print(f"Copied:   {copied_slotted_obj}")
    print(f"x from copied: {copied_slotted_obj.x}") # 期待通りにアクセスできる

    print("\n--- Testing MyHybridSlottedClass (will fall into __dict__ branch) ---")
    orig_hybrid_obj = MyHybridSlottedClass(100, "hello")
    copied_hybrid_obj = s_copy(orig_hybrid_obj)
    print(f"Original: {orig_hybrid_obj}")
    print(f"Copied:   {copied_hybrid_obj}")
    print(f"x from copied: {copied_hybrid_obj.x}")
    print(f"z from copied: {copied_hybrid_obj.z}") # __dict__ に入る属性もコピーされているはず

print()
print()
print("owari")
print()
print()


class MyClass:
    __slots__ = ['on_trigger']

    def __init__(self, value, callback_func):
        self.value = value
        self.on_trigger = callback_func # インスタンス変数に格納されたコールバック

    def do_something(self): # クラスに定義された通常のメソッド
        print("Doing something...")
        if self.on_trigger:
            self.on_trigger(self.value)

# --- テストと使用例 (先ほどの MyClass を使用) ---
if __name__ == '__main__':
    def my_callback(val):
        print(f"Callback triggered with value: {val}")

    original = MyClass(10, my_callback)
    print(dir(original))
    print("--- Original object ---")
    print(f"original.value: {original.value}")
    print(f"original.on_trigger: {original.on_trigger}")
    original.do_something()

    print("\n--- Copied object ---")
    copied = s_copy(original)
    print(f"{type(copied)=}")
    print(dir(copied))
    print(f"{copied.__dict__=}")
    print(f"{copied.value=}")
    print(f"copied.value: {copied.value}")
    print(f"copied.on_trigger: {copied.on_trigger}")
    copied.do_something() # これが正しく動作することを確認

    # コピー後の変更
    copied.value = 20
    print(f"copied.on_trigger is original.on_trigger: {copied.on_trigger is original.on_trigger}") # True (浅いコピーなので参照は共有)
    
    print("\n--- After modifying copied object ---")
    print(f"Original value: {original.value}")
    print(f"Copied value: {copied.value}")