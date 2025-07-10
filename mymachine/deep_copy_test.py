from mymachine import deep_copy

class Node:
    def __init__(self, name):
        self.name = name
        self.link = None

# 循環構造を作る
a = Node("A")
b = Node("B")
a.link = b
b.link = a

c = deep_copy(a)

print(c.name)                   # "A"
print(c.link.name)              # "B"
print(c.link.link.name)         # "A" （戻ってきてる！）
print(c is not a and c.link.link is c)  # True（循環コピー成功）