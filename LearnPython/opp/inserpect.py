# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 14:55
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : inserpect.py
import inspect


class Fa(object):
    def __init__(self):
        a = 1

    def f(self):
        print "ddd"

    def close(self):
        print "ddd"


b = inspect.getmembers(Fa)
print b
c = getattr(Fa, "a", None)
print c
