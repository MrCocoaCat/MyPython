# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 14:53
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : super.py



class A(object):
    def __init__(self):
        print('A')


class B(A):
    def __init__(self):
        print('B')
        super(B,self).__init__()


class C(A):
    def __init__(self):
        print('C')
        super(C,self).__init__()


class D(A):
    def __init__(self):
        print('D')
        super(D, self).__init__()


class E(B, C):
    def __init__(self):
        print('E')
        super(E, self).__init__()

        print("--",self.__class__.__name__)
e = E()