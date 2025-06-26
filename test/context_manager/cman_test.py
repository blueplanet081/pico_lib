class MyManager:
    def __init__(self, name="MyManager"):
        self.name = name
        self.iflag = False
        print(f"{self.name} Initialized. {self.iflag=}")
    
    def __enter__(self):
        print(f"{self.name} Enter called. {self.iflag=}")
        self.iflag = True
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(f"{self.name} Exit called. {self.iflag=}")
        self.iflag = False

mm = MyManager(name="OREORE")

print(f"{mm.iflag=}")

with mm:
    print("Hey You!")
    print(f"{mm.iflag=}")

print(f"{mm.iflag=}")

print()
print()
with MyManager(name="AREARE"):
    print("Hey Lady!")