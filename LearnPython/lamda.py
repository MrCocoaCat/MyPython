# -*- coding: UTF-8 -*-
stm = lambda x: 100 * x
a = stm(4)
print(a)

stm2 = lambda x, y, z:x+10*y+z
b = stm2(1, 2, 3)
print(b)

# 高阶函数
# 函数名即为一个变量


def funA(n):
    return n*10


def func(n, f):
    print(f(n))
    return f(n)*3


print(func(5, funA))


def mulTen(n):
    return n*10


ll = [i for i in range(10)]
print(ll)

l3 = map(mulTen, ll)
print(l3)

for i in l3:
    print(i)

print('*'*20)

# reduce 函数，要求指定的函数必须为两个参数
from functools import reduce


def myadd(x, y):
    return x + y

rst = reduce(myadd,[1,2,3,4,5,6])
print(rst)

print('*'*20)
# filter 函数，过滤函数
# 利用函数进行判断，这封函数返回值为布尔值
def isEven(a):
    return a % 2 == 0


l = [3, 6, 7, 8, 9, 20, 6, 8]
res=filter(isEven, l)
for i in res:
    print(i)


