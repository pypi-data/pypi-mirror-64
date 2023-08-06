def fubonachi(limit=1):
    a = 0
    b = 1
    res = [0, 1]
    for i in range(limit):
        a, b = b, a + b
        res.append(b)
    return res
