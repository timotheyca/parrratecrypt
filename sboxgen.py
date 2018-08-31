from binfieldv2 import *

Sbox = bytearray(256*[0])
InvSbox = bytearray(256*[0])

for i in range(256):
    Sbox[i] = (BinFieldElement(i, 8, '100011011') ** -1).simplify().value

#print(list(Sbox))
#print(len(set(Sbox)))

def cyclic_mul(a, b, m):
    return a * b % m + a * b // m


def cyclic_shift(a, b, m):
    return (a << b) % m + (a << b) // m

b_s = lambda a, b: cyclic_shift(a, b, 256)
someStrangeC = 99


def someStrangeFunc(b):
    global someStrangeC
    return b ^ b_s(b, 1) ^ b_s(b, 2) ^ b_s(b, 3) ^ b_s(b, 4) ^ someStrangeC


for i in range(256):
    Sbox[i] = someStrangeFunc(Sbox[i])


for i in range(256):
    InvSbox[Sbox[i]] = i


mul_arr = 15 * [[]]
for i in [1, 2, 3, 9, 11, 13, 14]:
    mul_arr[i] = bytearray(256 * [0])
    for j in range(256):
        mul_arr[i][j] = (BinFieldElement(j, 8, '100011011')  * BinFieldElement(i, 8, '100011011')).simplify().value


Rcon = [bytearray(4)]
curr = BinFieldElement(1, 8, '100011011')
step = BinFieldElement(2, 8, '100011011')
for i in range(10):
    Rcon.append(bytearray([curr.simplify().value, 0, 0, 0]))
    curr *= step


f = open('Sbox', 'w')
f.write(str(Sbox))
f.close()
f = open('InvSbox', 'w')
f.write(str(InvSbox))
f.close()
f = open('mul_arr', 'w')
f.write(str(mul_arr))
f.close()
f = open('Rcon', 'w')
f.write(str(Rcon))
f.close()