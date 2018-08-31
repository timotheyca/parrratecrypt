def fpm(x, p, m):
    out = 1
    for i in bin(p)[2:]:
        out *= out
        if int(i):
            out *= x
        if m:
            out %= m
    return out