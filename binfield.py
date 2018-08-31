class BinFieldElement():
    c_num = {
        1:                int('11', base=2),
        2:               int('111', base=2),
        3:              int('1011', base=2),
        4:             int('10011', base=2),
        5:            int('100101', base=2),
        6:           int('1000011', base=2),
        7:          int('10000011', base=2),
        8:         int('100011101', base=2),
        9:        int('1000010001', base=2),
        10:      int('10000001001', base=2),
        11:     int('100000000101', base=2),
        12:    int('1000001010011', base=2),
        16:int('10000000000101101', base=2),
    }
    
    
    def __init__(self, value: int, exp: int, polynomial=None):
        self.value = value
        self.exp = exp
        self.mod = 1 << exp
        self.polynomial = polynomial
    
    
    def full_val(self):
        self.simplify()
        return (self.value, self.exp)
    
    
    def type_val(self):
        return (self.exp, self.polynomial)
    
    
    def __str__(self):
        return 'BinFieldElement' + str(self.full_val())
    
    
    def simplify(self):
        if self.polynomial == None:
            while self.value >= self.mod:
                out = self % self.mod
                for i in range(self.exp):
                    if int(bin(BinFieldElement.c_num[self.exp])[2:][::-1][i]):
                        out += (self >> self.exp) << i
                self.value = out.value
        else:
            while self.value >= self.mod:
                out = self % self.mod
                for i in range(self.exp):
                    if int(self.polynomial[::-1][i]):
                        out += (self >> self.exp) << i
                self.value = out.value            
        return self
    
    
    def __mod__(self, b):
        if isinstance(b, int):
            return BinFieldElement(self.value % b, self.exp, self.polynomial)
        raise TypeError
    
    
    def __mul__(self, other):
        if isinstance(other, BinFieldElement):
            if other.type_val() == self.type_val():
                if other.value == 0:
                    return BinFieldElement(0, self.exp, self.polynomial)
                else:
                    return BinFieldElement(self.value * (other.value % 2), self.exp, self.polynomial) + (((other >> 1) * self) << 1)
            raise ValueError
        return other * self
    
    
    def __add__(self, other):
        return self ^ other
    
    
    def __sub__(self, other):
        return self ^ other
    
    
    def __xor__(self, other):
        if isinstance(other, BinFieldElement):
            if other.type_val() == self.type_val():
                return BinFieldElement(self.value ^ other.value, self.exp, self.polynomial)
            raise ValueError
        return other ^ self
    
    
    def __lshift__(self, b):
        return BinFieldElement(self.value << b, self.exp, self.polynomial).simplify()
    
    
    def __rshift__(self, b):
        return BinFieldElement(self.value >> b, self.exp, self.polynomial)
    
    
    def __pow__(self, p):
        if p == -1:
            return self.inverse()
        delta = self
        out = BinFieldElement(1, self.exp, self.polynomial)
        if p < 0:
            delta = delta.inverse()
            p = -p
        pow_s = bin(p)[2:]
        for i in pow_s:
            out *= out
            if int(i):
                out *= delta
        return out
    
    
    def inverse(self):
        return (self ** (self.mod - 2)).simplify()
    
    
    def __floordiv__(self, other):
        return self * (other ** (-1))
    
    
    def __truediv__(self, other):
        return self // other


class BinField():
    def __init__(self, exp, start=2, polynomial=None):
        self.size = 1 << exp
        self.elements = self.size * [0]
        self.elements[0] = BinFieldElement(0, exp, polynomial)
        self.e_indexes = self.size * [0]
        self.e_indexes[0] = 0
        if exp >= 1:
            self.elements[1] = BinFieldElement(1, exp, polynomial)
            self.e_indexes[1] = 1
        if exp >= 2:
            self.elements[2] = BinFieldElement(start, exp, polynomial)
            self.e_indexes[start] = 2
        for i in range(3, self.size):
            self.elements[i] = self.elements[2] * self.elements[i - 1]
            self.elements[i].simplify()
            self.e_indexes[self.elements[i].value] = i
    
    
    def __getitem__(self, index):
        return self.elements[index]
    
    
    def inverse(self, num, index=True):
        if index:
            if num < 2:
                return num
            return self.size - num + 1
        else:
            return self.elements[self.inverse(self.e_indexes[num])]


def stupidPolynomialGenerator(exp, start):
    BinFieldElement.c_num[exp] = (1 << exp) + 1
    test_binf = BinField(exp, start)
    while len(set(i.value for i in test_binf)) < test_binf.size:
        BinFieldElement.c_num[exp] += 2
        test_binf = BinField(exp, start)
    return test_binf