# scompare.py (scopy() と同レベルで動作することを想定)

def scompare(obj1, obj2):
    """
    2つのオブジェクトの浅いレベルでの内容を比較します。
    scopy() がコピーするのと同じインスタンス変数に基づいて比較を行います。

    Args:
        obj1: 比較する最初のオブジェクト。
        obj2: 比較する2番目のオブジェクト。

    Returns:
        bool: オブジェクトの浅い内容が一致すれば True、そうでなければ False。
              異なる型のオブジェクトの場合は False を返します。
    """
    # 1. 型の比較
    # 異なる型のオブジェクトは、浅い比較においても等しくないと判断します。
    if type(obj1) is not type(obj2):
        return False

    # 2. 組み込みのイミュータブル型の直接比較
    # これらの型は値が同じであれば等しいので、Pythonのデフォルトの比較に任せます。
    if isinstance(obj1, (int, float, str, bool, type(None))):
        return obj1 == obj2

    # 3. 組み込みのミュータブルコンテナ型の浅い比較
    # scopy() と同様に、要素レベルでの浅い比較を行います。
    if isinstance(obj1, list):
        if len(obj1) != len(obj2):
            return False
        # リストの各要素を直接比較 (これが「浅い」比較)
        for i in range(len(obj1)):
            if obj1[i] != obj2[i]:
                return False
        return True
    elif isinstance(obj1, dict):
        if len(obj1) != len(obj2):
            return False
        # キーと値のペアを直接比較
        for key, value in obj1.items():
            if key not in obj2 or obj2[key] != value:
                return False
        return True
    elif isinstance(obj1, set):
        # セットは順序がないため、部分集合と超集合の関係で比較します。
        # A == B ならば A.issubset(B) and B.issubset(A) が True になります。
        return obj1 == obj2
    elif isinstance(obj1, tuple):
        if len(obj1) != len(obj2):
            return False
        # タプルの各要素を直接比較
        for i in range(len(obj1)):
            if obj1[i] != obj2[i]:
                return False
        return True

    # 4. ユーザー定義クラスのインスタンスの比較
    # ここからが、scopy() の属性取得ロジックの応用です。

    # 比較対象の属性名を決定するヘルパー関数
    # この関数は scopy() の内部ロジック (_get_copyable_attrs) とほぼ同じです。
    def _get_comparable_attrs(obj):
        """オブジェクトから浅い比較の対象となる属性名のリストを取得する。"""
        if hasattr(obj.__class__, '_copy_attrs_'):
            # _copy_attrs_ があれば最優先
            return obj.__class__._copy_attrs_
        
        attrs_list = []
        if hasattr(obj, '__dict__'):
            # __dict__ にインスタンス変数がある場合
            for name in obj.__dict__.keys():
                # 特殊属性は比較対象外
                if not name.startswith('__'):
                    attrs_list.append(name)
        elif hasattr(obj.__class__, '__slots__'):
            # __slots__ にインスタンス変数がある場合
            for name in obj.__class__.__slots__:
                attrs_list.append(name)
        # else:
            # 警告: __dict__ も __slots__ もないクラスのインスタンスは、
            # 自動的に比較できるインスタンス属性を特定できません。
            # このケースでは、空のリストを返すか、エラーを発生させるか、
            # dir() を使って全属性を総当たりするかなどの判断が必要になります。
            # 現在は空リストを返します。

        return attrs_list

    attrs_to_compare = _get_comparable_attrs(obj1)

    # 各属性の値を比較
    for attr_name in attrs_to_compare:
        # 両方のオブジェクトがその属性を持っているか確認
        if not hasattr(obj1, attr_name) or not hasattr(obj2, attr_name):
            # どちらかに属性がない場合は等しくない
            return False
        
        # 属性値が異なる場合は等しくない
        # ここでの `!=` は、その属性値自体の `__eq__` メソッドを呼び出します。
        # これが「浅い」比較たる所以です。
        if getattr(obj1, attr_name) != getattr(obj2, attr_name):
            return False
    
    # 全ての比較対象属性が一致すれば等しい
    return True

# --- テストと使用例 ---
if __name__ == '__main__':
    # MyClass: __dict__ を持つクラス
    class MyClass:
        _copy_attrs_ = ('id', 'name', 'data_list') # 比較対象を明示

        def __init__(self, id, name, data_list):
            self.id = id
            self.name = name
            self.data_list = data_list # ミュータブルなリスト

        def __repr__(self):
            return f"MyClass(id={self.id}, name='{self.name}', data_list={self.data_list})"

    # MySlottedClass: __slots__ を持つクラス
    class MySlottedClass:
        __slots__ = ('x', 'y')
        def __init__(self, x, y):
            self.x = x
            self.y = y
        def __repr__(self):
            return f"MySlottedClass(x={self.x}, y={self.y})"

    # --- 組み込み型のテスト ---
    print("--- Built-in Types Comparison ---")
    print(f"scompare(10, 10): {scompare(10, 10)}")        # True
    print(f"scompare(10, 20): {scompare(10, 20)}")        # False
    print(f"scompare('a', 'a'): {scompare('a', 'a')}")    # True
    print(f"scompare('a', 'b'): {scompare('a', 'b')}")    # False
    print(f"scompare([1, 2], [1, 2]): {scompare([1, 2], [1, 2])}") # True
    print(f"scompare([1, 2], [1, 3]): {scompare([1, 2], [1, 3])}") # False
    print(f"scompare({'a': 1}, {'a': 1}): {scompare({'a': 1}, {'a': 1})}") # True
    print(f"scompare((1,2), (1,2)): {scompare((1,2), (1,2))}") # True
    print(f"scompare(10, '10'): {scompare(10, '10')}")    # False (型が異なる)

    # --- MyClass (__dict__) のテスト ---
    print("\n--- MyClass (__dict__) Comparison ---")
    list_a = [1, 2]
    list_b = [1, 2]
    list_c = [3, 4]

    obj1 = MyClass(1, "ItemA", list_a)
    obj2 = MyClass(1, "ItemA", list_b) # list_a と list_b は別オブジェクトだが内容が同じ
    obj3 = MyClass(1, "ItemA", list_c)
    obj4 = MyClass(2, "ItemA", list_a)
    
    # scopy() は別途定義が必要ですが、ここでは scompare() のみテスト
    # from scopy import scopy # scopy() が別ファイルにある場合
    # copied_obj1 = scopy(obj1) # scopy() を使う場合

    print(f"obj1: {obj1}")
    print(f"obj2: {obj2}")
    print(f"obj3: {obj3}")
    print(f"obj4: {obj4}")

    print(f"scompare(obj1, obj2): {scompare(obj1, obj2)}") # True (データ属性の値が一致)
    print(f"scompare(obj1, obj3): {scompare(obj1, obj3)}") # False (data_list の内容が異なる)
    print(f"scompare(obj1, obj4): {scompare(obj1, obj4)}") # False (id が異なる)
    print(f"scompare(obj1, obj1): {scompare(obj1, obj1)}") # True

    # コピーされたオブジェクトとの比較（scopy() の結果が想定通りなら True）
    # print(f"scompare(obj1, copied_obj1): {scompare(obj1, copied_obj1)}") # True となるはず

    # --- MySlottedClass (__slots__) のテスト ---
    print("\n--- MySlottedClass (__slots__) Comparison ---")
    s_obj1 = MySlottedClass(10, 20)
    s_obj2 = MySlottedClass(10, 20)
    s_obj3 = MySlottedClass(30, 40)

    print(f"s_obj1: {s_obj1}")
    print(f"s_obj2: {s_obj2}")
    print(f"s_obj3: {s_obj3}")

    print(f"scompare(s_obj1, s_obj2): {scompare(s_obj1, s_obj2)}") # True
    print(f"scompare(s_obj1, s_obj3): {scompare(s_obj1, s_obj3)}") # False

    # 異なる型の比較
    print(f"scompare(obj1, s_obj1): {scompare(obj1, s_obj1)}") # False (型が異なる)