# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 14:53
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : super.py


class A:
    obj_dic = {}

    def __init__(self):
        print('init A')
        self.a = 2

    @staticmethod
    def create(id):
        return A.obj_dic.setdefault(id, B(id))
        #return B(id)

    def mul(self):
        print(self.a**2)

    def __del__(self):
        print('del A')


class B(A):
    def __init__(self, id):
        print('init B')
        self.id = id
        super(B, self).__init__()

    def __del__(self):
        print('del B')


class C(A):
    def __init__(self):
        print('C')
        super(C, self).__init__()


if __name__ == '__main__':
    b = A.create(1)
    print(b)
    b.id = 888
    print(b.id)

    b = A.create(1)
    print(b)
    print(b.id)

    b = A.create(8)
    print(b)

    b = A.create(1)
    print(b)
    print(b.id)

    #b.mul()