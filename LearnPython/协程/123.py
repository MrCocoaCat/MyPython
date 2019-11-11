# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 18:53
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 123.py

import time


class A:
    def __init__(self):
        pass

    @staticmethod
    def fun(a):
        print(a)
        pass

    def funb(self, d):
        print(d)
        pass

class B:
    a = ''
    assert isinstance(a, str)


a = A()
a.fun(1)
a.funb(1)
exit(0)



print(id(a))
b = A()
print(id(b))




b = B()
b.a = 1
print("asdasdasd")

a = 11111111111111111111111111111111111111111111111111111111111111111111111111111111111111199999999999999999999999999999999999999999999999999999
print(type(a))
b = '11111111111111111111111111111111111111111111111111111111111111111111111111111111111111199999999999999999999999999999999999999999999999999999'
c = int(b)
print(c)
print(type(c))