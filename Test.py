from ecc import FieldElement, Point,G,N

#초기화 및 ==
# a = FieldElement(7,13)
# b = FieldElement(6,13)
# print(a!=b)
# print(a!=a)

#덧셈과 뺄셈
# a = FieldElement(7,13)
# b = FieldElement(12,13)
# c = FieldElement(8,13)

# print(a-b==c)

#곱셉과 거듭제곱
# print((95*45*31)%97)
# print((17*13*19*44)%97)
# print(((127%97)*77**49)%97)

#나눗셈
#3 /f 24
# prime = 31
# print(3 * pow(24,prime-2,prime) % prime)
# print(pow(pow(17,prime-2),3,prime))
# print(pow(pow(4,prime-2),4,prime) * 11 %prime)

# a = FieldElement(3,prime)
# b = FieldElement(24,prime)
# c = a/b
# print(c.num)

##타원곡선

#두 점이 다른경우
# a = Point(2,5,5,7)
# b = Point(-1,-1,5,7)
# c = a+b
# print(c.x,c.y)

#두 점이 같은 경우 (직선이 접하는 경우)
# a = Point(-1,-1,5,7)
# c = a+a
# print(c.x,c.y)

#유한체의 타원곡선
# a = FieldElement(num = 0, prime = 223)
# b = FieldElement(num = 7, prime = 223)
# x = FieldElement(num = 192, prime = 223)
# y = FieldElement(num = 105, prime = 223)
# p1 = Point(x,y,a,b)
# print(p1)p

# prime = 223
# a = FieldElement(num=0,prime = prime)
# b = FieldElement(num=7, prime = prime)

# x1 = FieldElement(num=170,prime=prime)
# y1 = FieldElement(142,prime)

# x2 = FieldElement(60,prime)
# y2 = FieldElement(139,prime)

# p1 = Point(x1,y1,a,b)
# p2 = Point(x2,y2,a,b)

# p3 = p1+p2

# print(p3.x,p3.y)

prime = 19
k = [1,3,7,18]
for num in k :
    print(sorted([num * i % prime for i in range(prime)]))
