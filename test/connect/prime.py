plist = []

def isprime(i):
    global plist
    for p in plist:
        if (i % p) == 0:
            return False
    else:
        plist.append(i)
        return True

print("start")
former = 0
s = set()
for i in range(2, 10000000):
    # print(plist)
    if isprime(i):
        if former:
            s.add(i - former)
        # print(i, f"({i - former if former else '-'})")
        print(i, f"{s}")
        former = i