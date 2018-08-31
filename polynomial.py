from auxmaths import *

class PrimeFieldElement:
    def __init__(self, value, p=2):
        if isinstance(value, int) and isinstance(p, int):
            self.value = value % p
            self.p = p
            return
        raise TypeError
    
    
    def __str__(self):
        return 'PFE' + str((self.value, self.p))
    
    
    def __int__(self):
        return self.value
    
    
    def create(self, value):
        return PrimeFieldElement(value, self.p)
    
    
    def __add__(self, other):
        if isinstance(other, PrimeFieldElement):
            if other.p == self.p:
                return self.create(self.value + other.value)
            raise ValueError
        return other + self
    
    
    def __neg__(self):
        return self.create(-self.value)
    
    
    def __sub__(self, other):
        if isinstance(other, PrimeFieldElement):
            if other.p == self.p:
                return self.create(self.value - other.value)
            raise ValueError
        return other + self        
    
    
    def __mul__(self, other):
        if isinstance(other, PrimeFieldElement):
            if other.p == self.p:
                return self.create(self.value * other.value)
            raise ValueError
        if isinstance(other, int):
            return self.create(self.value * other)
        return other * self
    
    
    def __pow__(self, other):
        out = self.create(1)
        for i in bin(other % self.p)[2:]:
            out *= out
            if int(i):
                out *= self
        return out
    
    
    def __truediv__(self, other):
        return self * (other ** -1)
    
    
    def __floordiv__(self, other):
        return self / other
    
    
    def __eq__(self, other):
        #print(type(self), type(other))
        if isinstance(other, PrimeFieldElement):
            return self.value == other.value and self.p == other.p
        return self == other

PFE = PrimeFieldElement


class Polynomial:
    def __init__(self, c_array:tuple, zero=0, one=1):
        #print(c_array)
        self.c_array = tuple(c_array)
        self.zero = zero
        self.one = one
        while self.c_array and (self.c_array[-1] == zero):
            self.c_array = self.c_array[:-1]
        if not self.c_array:
            self.c_array = (zero,)
        self.power = len(self.c_array) - 1
    
    
    def create(self, c_array):
        return Polynomial(c_array, self.zero, self.one)
    
    
    def __str__(self):
        return 'Polynomial' + str(([str(i) for i in self.c_array], 'zero=' + str(self.zero), 'one=' + str(self.one)))
    
    
    def __lshift__(self, other):
        return self.create((self.zero,) * other + self.c_array)
    
    
    def __rshift__(self, other):
        return self.create(self.c_array[other:])
    
    
    def __mul__(self, other):
        if isinstance(other, Polynomial):
            return sum([((self.c_array[i] * other) << i) for i in range(len(self.c_array))], self.create([self.zero]))
        return self.create([i * other for i in self.c_array])
    
    
    def __pow__(self, other):
        out = self.create([self.one])
        for i in bin(other)[2:]:
            out *= out
            if int(i):
                out *= self
        return out
    
    def __rmul__(self, other):
        return self * other
    
    
    def __add__(self, other):
        if isinstance(other, Polynomial):
            outp = max(self.power, other.power)
            ct1 = self.c_array + (self.zero,) * (outp - self.power)
            ct2 = other.c_array + (self.zero,) * (outp - other.power)
            return self.create((ct1[i] + ct2[i] for i in range(outp + 1)))
        return other + self
    
    
    def __neg__(self):
        return self * -(self.one)
    
    
    def __sub__(self, other):
        return self + (-other)
    
    
    #def __rmul__(self, other):
    #    return self * other
    
    
    #def __getitem__(self, i):
        #return self.c_array[i]
    
    
    def __divmod__(self, other):
        if isinstance(other, Polynomial):
            current = self
            divres = {}
            while current.power >= other.power:
                subres = current.c_array[-1] / other.c_array[-1]
                divres[current.power - other.power] = subres
                current -= (subres * other) << (current.power - other.power)
            divres_a = [self.zero] * (max(list(divres) + [0]) + 1)
            for i in list(divres):
                divres_a[i] = divres[i]
            return (self.create(divres_a), current)
        raise TypeError
    
    
    def __floordiv__(self, other):
        return divmod(self, other)[0]
    
    
    def __mod__(self, other):
        return divmod(self, other)[1]
    
    
    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.c_array == other.c_array
        return False
    
    
    def __getitem__(self, other):
        if isinstance(other, int):
            if other > self.power:
                return self.zero
            return self.c_array[0]
        if isinstance(other, slice):
            [self[i] for i in range((other.start or 0), (other.stop or (self.power + 1)), (other.step or 1))]


class LimitedFieldElement():
    def __init__(self, aval, amod, p=2):
        # pval and pmod are Polynomial of PrimeFieldElement
        self.aval = aval
        self.amod = amod
        pval = Polynomial([PrimeFieldElement(i, p) for i in aval], PrimeFieldElement(0, p), PrimeFieldElement(1, p))
        pmod = Polynomial([PrimeFieldElement(i, p) for i in amod], PrimeFieldElement(0, p), PrimeFieldElement(1, p))
        pval = (pval % pmod)
        self.aval = tuple([i.value for i in pval.c_array])
        self.amod = tuple([i.value for i in pmod.c_array])
        self.p = p
        self.n = len(amod) - 1
        self._pval = None
        self._pmod = None
        return
    
    
    def create(self, aval):
        return LimitedFieldElement(aval, self.amod, self.p)
    
    
    def pval(self):
        if self._pval == None:
            self._pval = Polynomial([PrimeFieldElement(i, self.p) for i in self.aval], PrimeFieldElement(0, self.p), PrimeFieldElement(1, self.p))
        return self._pval
    
    
    def pmod(self):
        if self._pmod == None:
            self._pmod = Polynomial([PrimeFieldElement(i, self.p) for i in self.amod], PrimeFieldElement(0, self.p), PrimeFieldElement(1, self.p))
        return self._pmod
    
    
    def __str__(self):
        return 'LFE' + str((self.aval, self.amod, self.p))
    
    
    def tval(self):
        return (self.amod, self.p)
    
    
    def __add__(self, other):
        if isinstance(other, LimitedFieldElement) and other.tval() == self.tval():
            pval1 = self.pval()
            pval2 = other.pval()
            pmod = self.pmod()
            pval = ((pval1 + pval2) % pmod)
            return self.create([i.value for i in pval.c_array])
        raise TypeError
    
    
    def __neg__(self):
        pval = self.pval()
        pval = -pval
        pmod = self.pmod()
        pval = (pval % pmod)
        return self.create([i.value for i in pval.c_array])
    
    
    def __sub__(self, other):
        return self + (-other)
    
    
    def __mul__(self, other):
        if isinstance(other, LimitedFieldElement) and other.tval() == self.tval():
            pval1 = self.pval()
            pval2 = other.pval()
            pmod = self.pmod()
            pval = ((pval1 * pval2) % pmod)
            return self.create([i.value for i in pval.c_array])
        return other * self
    
    
    def __pow__(self, other):
        out = self.create([1])
        for i in bin(other % (fpm(self.p, self.n, 0) - 2))[2:]:
            out *= out
            if int(i):
                out *= self
        return out
    
    
    def __truediv__(self, other):
        return self * (other ** -1)
    
    
    def __floordiv__(self, other):
        return self / other
    
    
    def __eq__(self, other):
        if isinstance(other, LimitedFieldElement):
            return self.p == other.p and self.amod == other.amod and self.aval == other.aval
        return False
LFE = LimitedFieldElement

#print(str(LimitedFieldElement(Polynomial([0, 1]), Polynomial([1, 1, 1]), 2, 2)))