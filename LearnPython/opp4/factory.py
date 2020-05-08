# -*- coding: utf-8 -*-
# @Time    : 2020/3/20 11:06
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : fun1.py

from opp4.method import A
from opp4.method import B


class Method:
    method_dic = {'a': A,
                  'b': B}

    @classmethod
    def get_method(cls, method_type):
        return cls.method_dic.setdefault(method_type, None)


if __name__ == '__main__':
    fun = Method.get_method('c')
    if fun is None:
        print('no this ')
    else:
        fun().action()

