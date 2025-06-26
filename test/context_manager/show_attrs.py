class MyClass:
    counter = 0

    def __init__(self, val, callback=None):
        self.value = val
        self.my_callback = callback # インスタンス変数に格納された関数

    def class_method(self): # クラスに定義されたメソッド
        print(f"Class method called with value: {self.value}")
        if self.my_callback:
            self.my_callback(self.value * 2)

    def __repr__(self):
        return f"MyClass(value={self.value}, my_callback={self.my_callback})"

def external_func(x):
    print(f"External function called with {x}")

# Test 1: 基本的な動作
print("--- Test 1: Basic Copy ---")
ori = MyClass(10, external_func)

ori.class_method()

print()
print("make new obj")

obj = object.__new__(ori.__class__)

print("original objedt")
print(f"{dir(ori)=}")
print()
print(f"{ori.__dict__=}")
print()
print(f"{hasattr(obj, '__dict__')=}")
print()
print()
print("new objedt")
print(f"{dir(obj)=}")
print()
print(f"{obj.__dict__=}")

print()
print()
print("show attributes")
attr_names = dir(ori)
for attr_name in attr_names:
    print(f"{attr_name}")
    attr_value = getattr(ori, attr_name)
    print(f"{dir(attr_value)=}")
    print(f"{hasattr(attr_value, '__class__')=}")
    print(f"{hasattr(attr_value, '__globals__')=}")
    print()
