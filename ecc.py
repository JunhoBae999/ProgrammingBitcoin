#유한체 원소 1개를 표현하는 클래스
from unittest import TestCase

class FieldElement :

    def __init__(self,num,prime) :
        if num >= prime or num < 0 :
            error = "Num {} not in field range 9 to {}".format(num,prime-1)
            raise ValueError(error)
        self.num = num
        self.prime = prime
    
    def __repr__(self) :
        return "FieldElement_{}({})".format(self.prime,self.num)
    
    def __eq__(self,other) :
        if other is None :
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self,other) :
        if other is None :
            return False
        return self.num != other.num or self.prime != other.prime
        # not (self == other)

    def __add__(self,other) :
        if self.prime != other.prime :
            raise TypeError('Cannot add two numbers in different Fields')
        num = (self.num+other.num) % self.prime
        return self.__class__(num,self.prime)
        #self.__clas__ 는 자기 자신의 클래스의 인스턴스를 반환. 즉, 새로 만듬
        #새로 FieldElement 할수도 있지만 그러면 상속되었을때 문제.
    def __sub__(self,other) :
            if self.prime != other.prime :
                raise TypeError('Cannot subtract two numbers in different Fields')
            num = (self.num-other.num) % self.prime
            return self.__class__(num,self.prime)
    
    def __mul__(self,other) :
        if self.prime != other.prime :
            raise TypeError("Cannot mulipy tow members in different Fields")
        num = (self.num * other.num) % self.prime
        return self.__class__(num,self.prime)
    
    def __pow__(self,exponent) :
        n = exponent % (self.prime-1)
        num = pow(self.num,n,self.prime)
        return self.__class__(num,self.prime)



    def __truediv__(self,other) :
        if self.prime != other.prime :
            raise TypeError("Cannot divide two members in different Fields")
        num = self.num * pow(other.num,other.prime-2,other.prime) % other.prime 
        return self.__class__(num,self.prime) 


class Point :
    def __init__(self,x,y,a,b) :
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        #무한대를 의미하는 none이 들어오면 방정식 확인 안함. 
        if self.x is None and self.y is None :
            return
        if self.y**2 != self.x**3 +a*x+b :
            raise ValueError('({},{})is not on the curve.'.format(x,y))
    
    def __eq__(self,other) :
        return self.x==other.x and self.y==other.y\
        and self.a==other.a and self.b == other.b
    
    def __ne__(self,other) :
        return not(self == other)
    
    #None 값은 무한대를 의미 - 덧셈의 항등원
    def __repr__(self):
            if self.x is None:
                return 'Point(infinity)'
            elif isinstance(self.x, FieldElement):
                return 'Point({},{})_{}_{} FieldElement({})'.format(
                    self.x.num, self.y.num, self.a.num, self.b.num, self.x.prime)
            else:
                return 'Point({},{})_{}_{}'.format(self.x, self.y, self.a, self.b)


    def __add__(self,other) :
        if self.a != other.a or self.b != other.b :
            raise TypeError("Points {}, {} are not on the same curve".format(self,other))
        #항등원에 대한 덧셈. None값이면 자기자신을 반환.
        if self.x is None :
            return other
        if other.x is None :
            return self
        #역원에 대한 덧셈 : 두 점은 x가 같고 y가 다른 경우이며 두 점을 이은 직선은 x축에 수직.
        if self.x == other.x and self.y != other.y :
            #반환결과는 무한원점. 
            return self.__class__(None,None,self.a,self.b)
        ##항등원과 역원에 대한 덧셈은 x축에 수직인 직선 두 점에 대한 연산.
        ##두 점이 점일 경우.
        if self.x != other.x :
            s = (other.y - self.y) / (other.x - self.x)
            newx = s**2 - self.x - other.x
            newy = s*(self.x - newx) - self.y 
            return self.__class__(newx,newy,self.a,self.b)
        
        if self == other :
            s = (3*self.x**2 + self.a) / 2*self.y
            newx = s**2 - 2*self.x
            newy = s *(self.x - newx) - self.y
            return self.__class__(newx,newy,self.a,self.b)
        
        #두 점이 같고 y좌표가 0이면 : 접선이 x축에 수직인 경우
        if self == other and self.y == 0 *self.x  :
            return self.__class__(None,None,self.a,self.b)
    
    def __rmul__(self,coefficient) :
        coef = coefficient
        current = self
        result = self.__class__(None,None,self.a,self.b)
        while coef :
            if coef & 1 :
                result +=  current
            current += current
            coef >>= 1
        return result


class ECCTest(TestCase) :
    
    def test_on_curve(self) :
        prime = 223
        a = FieldElement(0,prime)
        b = FieldElement(7,prime)
        valid_points = ((192,105),(17,56),(1,193))
        invalid_points = ((200,119),(42,99))
        for x_raw, y_raw in valid_points :
            x = FieldElement(x_raw,prime)
            y = FieldElement(y_raw,prime)
            Point(x,y,a,b)
            for x_raw, y_raw in invalid_points :
                x = FieldElement(x_raw,prime)
                y = FieldElement(y_raw,prime)
                with self.assertRaises(ValueError) :
                    Point(x,y,a,b)

P = 2**256 - 2**32-977
#secp256k1 유한체
class S56Field(FieldElement) :

    def __init__(self,num,prime = None):
        super().__init__(num=num,prime=P)

    def __repr__(self) :
        return '{:x}'.format(self.num).zfill(64)

A=0
B=7
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

class S256Point(Point) :

    def __init__(self,x,y,a=None,b=None) :
        a,b = S56Field(A),S56Field(B)
        if type(x) == int :
            super().__init__(x=S56Field(x),y=S56Field(y),a=a,b=b)
        else :
            super().__init__(x=x,y=y,a=a,b=b)

    def __rmul__(self,coefficient) :
       coef = coefficient % N
       return super().__rmul__(coef)

G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
