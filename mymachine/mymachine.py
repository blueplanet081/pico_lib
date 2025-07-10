BUILTIN_TYPES = (int, float, str, bool, list, tuple, dict, set, bytes, bytearray, range)

def s_compare(obj1, obj2) -> bool:
    ''' 二つのオブジェクトの内容を浅いレベルで比較する
    
    args:
      obj1: 比較するオブジェクト1
      obj2: 比較するオブジェクト2
    
    return:
      内容が同一なら True、違いがあるなら False
    '''

    if type(obj1) != type(obj2):
        return False

    if isinstance(obj1, BUILTIN_TYPES):
        return obj1 == obj2

    if hasattr(obj1, '__dict__') and hasattr(obj2, '__dict__'):
        return s_compare(obj1.__dict__, obj2.__dict__)

    if hasattr(obj1, '__slots__') and hasattr(obj2, '__slots__'):
        try:
            slots_a = obj1.__slots__
            slots_b = obj2.__slots__

            # 文字列またはタプルとしてスロット定義を比較
            if isinstance(slots_a, str):
                slots_a = (slots_a,)
            if isinstance(slots_b, str):
                slots_b = (slots_b,)

            if set(slots_a) != set(slots_b):
                return False

            for slot in slots_a:
                if not s_compare(getattr(obj1, slot, None), getattr(obj2, slot, None)):
                    return False
            return True
        except Exception:
            return False

    return False


def s_copy(obj):
    ''' オブジェクトの shallow copy を行う '''

    # 組み込みのミュータブル型をコピー
    if isinstance(obj, list):
        return obj[:]  # スライスによるコピー
    elif isinstance(obj, dict):
        return {k: v for k, v in obj.items()}  # 明示的なコピー
    elif isinstance(obj, set):
        return set(obj)
    elif isinstance(obj, bytearray):
        return bytearray(obj)

    # タプルはイミュータブルだが、要素がミュータブルな場合があるので再構成（浅いコピー）
    elif isinstance(obj, tuple):
        return tuple(obj)

    # 自作クラス（__dict__ベース）
    elif hasattr(obj, '__dict__'):
        cls = obj.__class__
        newobj = object.__new__(cls)  # __init__ は呼ばない
        for key in obj.__dict__:
            setattr(newobj, key, getattr(obj, key))
        return newobj

    # __slots__ベースのクラス
    elif hasattr(obj, '__slots__'):
        cls = obj.__class__
        newobj = object.__new__(cls)
        slots = obj.__slots__

        # 文字列1つの定義にも対応
        if isinstance(slots, str):
            slots = (slots,)
        for slot in slots:
            if hasattr(obj, slot):
                setattr(newobj, slot, getattr(obj, slot))
        return newobj

    # イミュータブル型はそのまま返してOK
    else:
        return obj


def deep_copy(obj, memo=None):
    ''' オブジェクトの deep copy を行う '''

    if memo is None:
        memo = {}

    obj_id = id(obj)
    if obj_id in memo:
        return memo[obj_id]

    # イミュータブル型
    if isinstance(obj, (int, float, str, bool, bytes, range, type(None))):
        return obj

    # tuple（要素を再帰コピー）
    if isinstance(obj, tuple):
        copied = tuple(deep_copy(item, memo) for item in obj)
        memo[obj_id] = copied
        return copied

    # list
    if isinstance(obj, list):
        copied = [deep_copy(item, memo) for item in obj]
        memo[obj_id] = copied
        return copied

    # dict
    if isinstance(obj, dict):
        copied = {}
        memo[obj_id] = copied
        for k, v in obj.items():
            copied[deep_copy(k, memo)] = deep_copy(v, memo)
        return copied

    # set
    if isinstance(obj, set):
        copied = set()
        memo[obj_id] = copied
        for item in obj:
            copied.add(deep_copy(item, memo))
        return copied

    # bytearray
    if isinstance(obj, bytearray):
        copied = bytearray(obj)
        memo[obj_id] = copied
        return copied

    # __dict__を持つカスタムオブジェクト
    if hasattr(obj, '__dict__'):
        cls = obj.__class__
        newobj = object.__new__(cls)
        memo[obj_id] = newobj
        for key in obj.__dict__:
            setattr(newobj, key, deep_copy(getattr(obj, key), memo))
        return newobj

    # __slots__ を持つオブジェクト
    if hasattr(obj, '__slots__'):
        cls = obj.__class__
        newobj = object.__new__(cls)
        memo[obj_id] = newobj
        slots = obj.__slots__
        if isinstance(slots, str):
            slots = (slots,)
        for slot in slots:
            if hasattr(obj, slot):
                setattr(newobj, slot, deep_copy(getattr(obj, slot), memo))
        return newobj

    # 対応外 → そのまま返す（または例外にする）
    return obj
