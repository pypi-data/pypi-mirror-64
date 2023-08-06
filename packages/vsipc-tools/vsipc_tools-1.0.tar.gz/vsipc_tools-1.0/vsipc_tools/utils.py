import time


def fubonachi(limit=1):
    a = 0
    b = 1
    res = [0]
    for i in range(limit):
        res.append(a * b)
        a, b = b, a + b
        time.sleep(1)
    return res
