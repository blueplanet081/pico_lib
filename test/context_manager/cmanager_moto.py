import time

class ThisClass:
    def __init__(self, name="DefaultThisClass"):
        self.name = name
        self._is_active = False # このクラスの内部状態フラグ
        print(f"[{self.name}] ThisClass インスタンスを初期化しました。")

    class _ProcessContextManager:
        """
        ThisClass の内部処理を管理するコンテキストマネージャ。
        通常はThisClassのメソッドからのみアクセスされることを想定。
        """
        def __init__(self, parent_instance):
            self.parent = parent_instance
            print(f"[{self.parent.name}] _ProcessContextManager を初期化しました。")

        def __enter__(self):
            """
            with ブロックに入る際に呼び出されます。
            親インスタンスの処理を開始状態にします。
            """
            print(f"[{self.parent.name}] __enter__() が呼び出されました。処理を開始します。")
            if self.parent._is_active:
                raise RuntimeError(f"[{self.parent.name}] 既にアクティブな処理が存在します。")
            self.parent._is_active = True
            print(f"[{self.parent.name}] _is_active: {self.parent._is_active}")
            return self.parent # with ... as の後に親インスタンスを渡す

        def __exit__(self, exc_type, exc_value, traceback):
            """
            with ブロックを抜ける際に呼び出されます。
            親インスタンスの処理を終了状態にします。
            """
            print(f"[{self.parent.name}] __exit__() が呼び出されました。処理を終了します。")
            self.parent._is_active = False
            print(f"[{self.parent.name}] _is_active: {self.parent._is_active}")

            if exc_type is not None:
                print(f"[{self.parent.name}] 例外が発生しました: {exc_type.__name__}: {exc_value}")
                # 例外を再発生させる
                return False
            return False

    def Process(self):
        """
        with 構文で使用されるコンテキストマネージャのインスタンスを返します。
        このメソッドを呼び出すことで、with ... as の準備ができます。
        """
        print(f"[{self.name}] Process() メソッドが呼び出されました。")
        return self._ProcessContextManager(self)

    # ThisClass の他のメソッド
    def perform_task(self):
        """ThisClass の他のタスクを実行するメソッド（処理中フラグを確認）。"""
        if self._is_active:
            print(f"[{self.name}] アクティブな処理中にタスクを実行しています。")
            time.sleep(0.05)
        else:
            print(f"[{self.name}] (警告) アクティブな処理中でないのにタスクを実行しようとしました。")


# --- 使用例 ---

print("--- シナリオ1: 正常な処理 ---")
my_instance = ThisClass("メイン処理")
print(f"初期状態: _is_active = {my_instance._is_active}")

with my_instance.Process() as main_process:
    # with ブロック内では main_process は my_instance と同じオブジェクト
    print(f"with ブロック内: _is_active = {main_process._is_active}")
    main_process.perform_task() # 親インスタンスのメソッドを呼び出す
    print(f"[{main_process.name}] 何らかのメイン処理を実行中...")
    time.sleep(0.1)
    main_process.perform_task()
    # 必要であれば、with ... as で受け取ったオブジェクト自体も利用できる
    print(f"with ブロック終了直前: _is_active = {my_instance._is_active}")

print(f"with ブロック後: _is_active = {my_instance._is_active}")


print("\n--- シナリオ2: 例外が発生する処理 ---")
another_instance = ThisClass("エラー処理")
print(f"初期状態: _is_active = {another_instance._is_active}")

try:
    with another_instance.Process() as error_process:
        print(f"with ブロック内: _is_active = {error_process._is_active}")
        print(f"[{error_process.name}] エラーを引き起こす処理を実行中...")
        time.sleep(0.05)
        raise ValueError("意図的なエラー") # 例外を発生させる
except ValueError as e:
    print(f"外部で例外を捕捉しました: {e}")

print(f"with ブロック後 (例外): _is_active = {another_instance._is_active}")


print("\n--- シナリオ3: 入れ子処理の試み (不正な使用) ---")
# 同じインスタンスで複数の Process を入れ子にするとエラーになるように設計
third_instance = ThisClass("多重処理")
print(f"初期状態: _is_active = {third_instance._is_active}")

try:
    with third_instance.Process():
        print(f"[{third_instance.name}] 外側の処理がアクティブ: {third_instance._is_active}")
        time.sleep(0.05)
        with third_instance.Process(): # ここでエラーが発生するはず
            print(f"[{third_instance.name}] 内側の処理がアクティブ: {third_instance._is_active}")
except RuntimeError as e:
    print(f"外部でエラーを捕捉しました: {e}")

print(f"with ブロック後 (エラー発生): _is_active = {third_instance._is_active}")