class Epacket:
    def __init__(self, contents, send=False) -> None:
        self.contents = contents
        self.send: bool = send
        self._is_active = False

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



    def receive(self):
        if self.send:
            self.send = False
            return self.contents
        else:
            return None

    def send(self, contents=None):




