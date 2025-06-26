def copy(obj):
    """
    MicroPython向けの簡易的な shallow copy 実装。
    標準の copy.copy() の機能の一部を模倣します。
    """
    # 1. 組み込みのミュータブルコンテナの特殊処理 (以前と同じ)
    if isinstance(obj, list):
        return obj[:]
    elif isinstance(obj, dict):
        return obj.copy()
    elif isinstance(obj, set):
        return obj.copy()
    elif isinstance(obj, tuple):
        return tuple(obj)
    elif isinstance(obj, (int, float, str, bool, type(None))):
        return obj

    # 2. ユーザー定義クラスのインスタンスに対する処理
    # __copy__ メソッドが定義されていればそれを使用
    if hasattr(obj, '__copy__'):
        return obj.__copy__()

    # 新しい空のインスタンスを作成
    # __init__ を呼び出さない object.__new__ を使用するのが安全
    new_obj = object.__new__(obj.__class__)

    # 3. インスタンスの属性をコピーする主要ロジック
    # __dict__ を持つクラスの場合
    if hasattr(obj, '__dict__'):
        print("obj has __dict__")
        # obj.__dict__ の内容をループして一つずつコピー
        for attr_name, attr_value in obj.__dict__.items():
            # setattr を使用して新しいオブジェクトに属性を設定
            # object.__setattr__ を使うことで、カスタムの __setattr__ をバイパスできます。
            object.__setattr__(new_obj, attr_name, attr_value)

    # __slots__ のみで __dict__ を持たないクラスの場合
    # __slots__ はクラス属性なので obj.__class__.__slots__ でアクセス
    # __slots__ のみで __dict__ を持たないクラスの場合 (elif を使うことで排他的に処理)
    elif hasattr(obj.__class__, '__slots__'):
        print("obj has __slots__ (and no __dict__ for instance vars)")
        for attr_name in obj.__class__.__slots__:
            # スロットに定義されている属性のみをコピー
            # 元オブジェクトがそのスロット属性を持っているか確認 (設定されていない場合もあるため)
            if hasattr(obj, attr_name):
                attr_value = getattr(obj, attr_name)
                object.__setattr__(new_obj, attr_name, attr_value)

    else:
        # __dict__も__slots__も明示的に見つからない場合のフォールバック（例: 組み込みのC拡張オブジェクトなど）
        # このケースは非常に稀ですが、もしこのようなオブジェクトをコピーする必要がある場合、
        # dir() を使った慎重な推測が必要になります。
        # 現在のMicroPythonの課題を考慮すると、_copy_attrs_ をクラスに実装してもらうのが一番安全です。
        print("Warning: Neither __dict__ nor __slots__ found for instance variables. "
              "Automatic attribute copying might be incomplete or incorrect.")
        # このブロックでは、何もしないか、あるいは dir() を使って可能な限り属性を推測するロジックをここに書く。
        # 例:
        # for attr_name in dir(obj):
        #     if not attr_name.startswith('__') and not callable(getattr(obj.__class__, attr_name, None)):
        #         if hasattr(obj, attr_name):
        #             object.__setattr__(new_obj, attr_name, getattr(obj, attr_name))

    # デバッグ用にコピー後の__dict__を表示
    # __slots__専用クラスの場合、new_obj.__dict__ は存在しない（または空）なので注意
    if hasattr(new_obj, '__dict__'):
        print(f"{new_obj.__dict__=}")
    else:
        print("New object does not have __dict__ attribute for instance variables.")

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
    copied_dict_obj = copy(orig_dict_obj)
    print(f"Original: {orig_dict_obj}")
    print(f"Copied:   {copied_dict_obj}")
    print(f"a from copied: {copied_dict_obj.a}") # 期待通りにアクセスできる

    print("\n--- Testing MySlottedClass ---")
    orig_slotted_obj = MySlottedClass(10, 20)
    copied_slotted_obj = copy(orig_slotted_obj)
    print(f"Original: {orig_slotted_obj}")
    print(f"Copied:   {copied_slotted_obj}")
    print(f"x from copied: {copied_slotted_obj.x}") # 期待通りにアクセスできる

    print("\n--- Testing MyHybridSlottedClass (will fall into __dict__ branch) ---")
    orig_hybrid_obj = MyHybridSlottedClass(100, "hello")
    copied_hybrid_obj = copy(orig_hybrid_obj)
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
    copied = copy(original)
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