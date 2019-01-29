# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 10:13
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : test.py


import eventlet
import time


def test(s):
    print(s + " begin")
    time.sleep(1)
    print(s + " end")

def testB(s):
    print(s + " begin")
    time.sleep(1)
    print(s + " end")

a = []
pool = eventlet.GreenPool(5)
a = time.time()
for i in range(5):
    pool.spawn(test(str(i)))
    pool.spawn(testB(str(i)))
b = time.time()
print b - a



