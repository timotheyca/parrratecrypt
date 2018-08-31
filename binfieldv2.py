class BinFieldElement():
    def __init__(self, value: int, exp: int, polynomial):
        self.value = value
        self.exp = exp
        self.mod = 1 << exp
        self.polynomial = polynomial
    
    
    def create(self, value):
        return BinFieldElement(value, self.exp, self.polynomial)
    
    
    def full_val(self):
        self.simplify()
        return (self.value, self.exp)
    
    
    def type_val(self):
        return (self.exp, self.polynomial)
    
    
    def __str__(self):
        return 'BinFieldElement' + str(self.full_val())
    
    
    def simplify(self):
        while self.value.bit_length() > self.exp:
            #out = self % self.mod
            #for i in range(self.exp):
            #    if int(self.polynomial[::-1][i]):
            #        out += (self >> self.exp) << i
            #self.value = out.value            
            self.value = (self.create((self.value // self.mod)) * self.create(int(self.polynomial, base=2)) + self).value
        return self
    
    
    def __mod__(self, b):
        if isinstance(b, int):
            return self.create(self.value % b)
        raise TypeError
    
    
    def __mul__(self, other):
        if isinstance(other, BinFieldElement):
            if other.type_val() == self.type_val():
                if other.value == 0 or self.value == 0:
                    return self.create(0)
                else:
                    return self.create(self.value * (other.value % 2)) + (((other >> 1) * self) << 1)
            raise ValueError
        elif isinstance(other, int):
            return self * self.create(other)
        return other * self
    
    
    def __add__(self, other):
        return self ^ other
    
    
    def __sub__(self, other):
        return self ^ other
    
    
    def __xor__(self, other):
        if isinstance(other, BinFieldElement):
            if other.type_val() == self.type_val():
                return self.create(self.value ^ other.value)
            raise ValueError
        return other ^ self
    
    
    def __lshift__(self, b):
        return self.create(self.value << b)
    
    
    def __rshift__(self, b):
        return self.create(self.value >> b)
    
    
    def __pow__(self, p):
        p %= (self.mod - 1)
        out = self.create(1)
        pow_s = bin(p)[2:]
        for i in pow_s:
            out *= out
            if int(i):
                out *= self
            out.simplify()
        return out
    
    
    def __floordiv__(self, other):
        return self * (other ** (-1))
    
    
    def __truediv__(self, other):
        return self // other
    
    
    def __getitem__(self, i):
        return (self.value >> i) % 2
    
    
    def __int__(self):
        return self.value