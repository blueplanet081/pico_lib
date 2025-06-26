class Epack:
    class _send:
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

    def __init__(self, value=None) -> None:
        self.value = value
        self.sended = False
        pass

    def has_arrived(self):
        return self.sended

    def receive(self):
        if self.sended:
            self.sended = False
            return self.value
        else:
            return None

    def send(self, value=None):
        if value is not None:
            self.value


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