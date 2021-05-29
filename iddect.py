import hashlib
def calHash(num):
    num = num+"2021"
    print(num)
    num = num.encode("utf-8")
    res = hashlib.md5(num)
    res = res.hexdigest()
    return res

if __name__ == "__main__":
    a =calHash("12341234")
    print(a)