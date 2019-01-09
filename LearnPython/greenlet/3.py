# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 9:51
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 3.py
import greenlet


def test1(x, y):
    print x,y
    try:
        z = gr2.switch(x+y)
    #  捕获不到异常
    except Exception:
        print 'catch Exception in test1'


def test2(u):
    assert False


gr1 = greenlet.greenlet(test1)
gr2 = greenlet.greenlet(test2)

try:
    gr1.switch("hello", " world")
except:
    print 'catch Exception in main'

