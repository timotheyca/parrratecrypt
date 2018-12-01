f = open('Sbox', 'r')
Sbox = eval(f.read())
f.close()
f = open('InvSbox', 'r')
InvSbox = eval(f.read())
f.close()
f = open('mul_arr', 'r')
mul_arr = eval(f.read())
f.close()
f = open('Rcon', 'r')
Rcon = eval(f.read())
f.close()


def vis():
    for i in range(4):
        print(' '.join([hex(_state[i*4+j] + 256)[3:] for j in range(4)]))


def SubBytes(state:bytearray):
    for i in range(16):
        state[i] = Sbox[state[i]]


def InvSubBytes(state):
    for i in range(16):
        state[i] = InvSbox[state[i]]


def ShiftRows(state):
    for i in range(4):
        state[i*4:i*4+4] = state[i*5:i*4+4]+state[i*4:i*5]


def InvShiftRows(state):
    for i in range(4):
        state[i*4:i*4+4] = state[i*3+4:i*4+4]+state[i*4:i*3+4]


def MixColumns(state):
    for i in range(4):
        c = [state[j*4+i] for j in range(4)]
        state[i + 0] = mul_arr[2][c[0]] ^ mul_arr[3][c[1]] ^ c[2] ^ c[3]
        state[i + 4] = mul_arr[2][c[1]] ^ mul_arr[3][c[2]] ^ c[3] ^ c[0]
        state[i + 8] = mul_arr[2][c[2]] ^ mul_arr[3][c[3]] ^ c[0] ^ c[1]
        state[i +12] = mul_arr[2][c[3]] ^ mul_arr[3][c[0]] ^ c[1] ^ c[2]


def InvMixColumns(state):
    for i in range(4):
        c = [state[j*4+i] for j in range(4)]
        state[i + 0] = mul_arr[14][c[0]] ^ mul_arr[11][c[1]] ^ mul_arr[13][c[2]] ^ mul_arr[9][c[3]]
        state[i + 4] = mul_arr[14][c[1]] ^ mul_arr[11][c[2]] ^ mul_arr[13][c[3]] ^ mul_arr[9][c[0]]
        state[i + 8] = mul_arr[14][c[2]] ^ mul_arr[11][c[3]] ^ mul_arr[13][c[0]] ^ mul_arr[9][c[1]]
        state[i +12] = mul_arr[14][c[3]] ^ mul_arr[11][c[0]] ^ mul_arr[13][c[1]] ^ mul_arr[9][c[2]]


def KeyExpansion(key:bytearray, Nk:int, Nr:int, Nb=4):
    w = Nb * (Nr + 1) * bytearray(4)
    for i in range(Nk):
        w[i*4:i*4+4] = bytearray([key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]])
    for i in range(Nk, Nb * (Nr+1)):
        temp = w[i*4-4:i*4]
        if i % Nk == 0:
            temp = [Sbox[temp[(j+1) % 4]] ^ Rcon[i // Nk][j] for j in range(4)]
        elif Nk > 6 and i % Nk == 4:
            temp = [Sbox[j] for j in temp]
        w[i*4:i*4+4] = [w[4*i+j] ^ temp[j] for j in range(4)]
    return w


def AddRoundKey(state, rkey):
    for i in range(16):
        state[i] ^= rkey[i]


def Cipher(in_b:bytearray, w:bytearray, Nr:int, Nb=4):
    state = bytearray(in_b)
    
    AddRoundKey(state, w[:Nb*4])
    
    for r in range(1, Nr):
        SubBytes(state)
        ShiftRows(state)
        MixColumns(state)
        AddRoundKey(state, w[r*Nb*4:(r+1)*Nb*4])
    
    SubBytes(state)
    ShiftRows(state)
    AddRoundKey(state, w[Nr*Nb*4:(Nr+1)*Nb*4])
    
    return state


def InvCipher(in_b:bytearray, w:bytearray, Nr:int, Nb=4):
    state = bytearray(in_b)
    
    AddRoundKey(state, w[Nr*Nb*4:(Nr+1)*Nb*4])
    
    for r in range(Nr - 1, 0, -1):
        InvShiftRows(state)
        InvSubBytes(state)
        AddRoundKey(state, w[r*Nb*4:(r+1)*Nb*4])
        InvMixColumns(state)
    
    InvShiftRows(state)
    InvSubBytes(state)
    AddRoundKey(state, w[:Nb*4])
    
    return state