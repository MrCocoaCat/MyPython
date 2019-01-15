# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 14:55
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : inspect.py

# import inspect


class Fa(object):
    def __init__(self):
        self.a = 1
        print self.__class__
        print hasattr(self.__class__, 'LOGGER_NAME')

    def f(self):
        print "ddd"

    def close(self):
        print "ddd"


# b = inspect.getmembers(Fa)
# print b
A = Fa()
c = getattr(A, "a", None)
#c = getattr(A, "a", None)

#print c
