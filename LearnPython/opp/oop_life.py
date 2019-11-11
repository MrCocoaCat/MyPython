# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 14:53
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : super.py
import abc
import six


class TEA:
    def __init__(self):
        print("init TEA")
        self.a = 123

    def ff(self):
        print("dsds")


@six.add_metaclass(abc.ABCMeta)
class A:
    obj_dic = {}

    def __init__(self):
        print('init A')
        self.a = 2
        self.b = TEA()

    @staticmethod
    def create(id):
        if id in A.obj_dic.keys():
            return A.obj_dic[id]
        else:
            A.obj_dic.setdefault(id, B(id))
            return A.obj_dic[id]

    @abc.abstractmethod
    def mul(self):
        pass

    def __del__(self):
        print('del A')


class B(A):
    def __init__(self, id):
        print('init B')
        self.id = id
        super(B, self).__init__()

    def __del__(self):
        print('del B')

    def mul(self):
        print(self.id ** 2)

    def tea(self):
        print(self.b)

    # def __str__(self):
    #   return str(self.__class__) + str(hex(id(self)))

    #def __repr__(self):
    #    return str(self.id)



class C(A):
    def __init__(self):
        print('C')
        super(C, self).__init__()


if __name__ == '__main__':

    #a = A()
    b = A.create(1)
    print(b)
    b.id = 888
    print(20 * "*")
    #b.tea()
    #print(b.id)

    b = A.create(1)
    print(b)
    print(20 * "*")
    #b.tea()
    #print(b.id)

    b = A.create(8)
    #b.tea()
    print(b)
    print(20 * "*")

    b = A.create(1)
    print(b)
    #b.tea()
    #print(b.id)
    print(20*"*")
    print(A.obj_dic)
    #b.mul()