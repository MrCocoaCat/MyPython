# -*- coding: utf-8 -*-
# @Time    : 2019/11/7 10:05
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : clas.py


class A:
    def __init__(self):
        self.x = None
        self.y = None

    def __str__(self):
        return str(self.__dict__)


class B:
    __slots__ = ("x", "y")


a = A()
a.x = 1
a.y = 2
print(a)


b = B()
b.x = 1
b.y = 2
print(b)
