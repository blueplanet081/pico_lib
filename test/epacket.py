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

class Epacket:
    def __init__(self, contents, send=False) -> None:
        self.contents = contents
        self._locked: bool = False
        self._is_empty: bool = True
        self._is_received: bool = True

    class _PackingContextManager:
        ''' with構文を使ってturnの開始を一時的にfreezeさせるクラス '''
        def __init__(self, parent_instance):
            self.parent = parent_instance

        def __enter__(self):
            if self.parent._is_active:
                raise RuntimeError(f"[{self.parent.name}] A process is already active.")
            self.parent._is_active = True
            print(f"[{self.parent.name}] _is_active: {self.parent._is_active}")
            return self.parent # with ... as の後に親インスタンスを渡す
            
        def __exit__(self, exc_type, exc_value, traceback):
            print(f"[{self.parent.name}] __exit__() が呼び出されました。処理を終了します。")
            self.parent._is_active = False
            print(f"[{self.parent.name}] _is_active: {self.parent._is_active}")

            if exc_type is not None:
                print(f"[{self.parent.name}] 例外が発生しました: {exc_type.__name__}: {exc_value}")
                # 例外を再発生させる
                return False
            return False

    def Packing(self):
        """
        with 構文で使用されるコンテキストマネージャのインスタンスを返します。
        このメソッドを呼び出すことで、with ... as の準備ができます。
        """
        print(f"[{self}] Process() メソッドが呼び出されました。")
        return self._PackingContextManager(self)

    def is_empty(self):
        return self._is_empty

    def send(self, contents, overwrite=False):
        if self._locked:
            return -1
        self._locked = True

        if self._is_empty or overwrite:
            self.contents = s_copy(contents)
            self._is_empty = False
            self._is_received = False
            self._locked = False
            return 1
        else:
            self._locke = False
            return 0

    def receive(self):
        if self._locked:
            return None
        self._locked = True

        if self._is_empty:
            self._locked = False
            return None

        if self._locked or self._is_empty:
            return None
        ret = s_copy(self.contents)

        



        if self.send:
            self.send = False
            return self.contents
        else:
            return None





