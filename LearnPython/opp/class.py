# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 13:33
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : class.py


class A:
    _id = 1234

    def __init__(self):
        self.x = 1
        self.y = 2


class B(A):
    pass


b = B()
print(isinstance(b, A))
