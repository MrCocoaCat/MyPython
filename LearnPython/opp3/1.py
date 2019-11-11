# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 16:12
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 1.py


class A:
    def __init__(self, num):
        self.num = num

    def add(self, a, b):
        return a+b + self.num

    def add2(self, a, b, c):
        return a + b + self.num+c

    def mul(self, a, b):
        return a*b + self.num

    def do_add(self, a, b, method):
        print(method(a, b, c))


def method(fun, a=None, b=None, c=None):
    if fun.__name__ == 'add':
        return fun(a, b)

    if fun.__name__ == 'add2':
        return fun(a, b, c)



aa = A(123)
print(aa.add.__name__)
method(aa.add)

#f = method(aa.add, 1, 2, 7)
#aa.do_add(1, 2, )