# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 9:52
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 2.py
import greenlet
def test1(x, y):
    print x,y
    print id(greenlet.getcurrent()), id(greenlet.getcurrent().parent) # 40240272 40239952
    z = gr2.switch(x+y)
    print 'back z', z

def test2(u):
    print u
    print id(greenlet.getcurrent()), id(greenlet.getcurrent().parent) # 40240352 40239952
    return 'hehe'

gr1 = greenlet.greenlet(test1)
gr2 = greenlet.greenlet(test2)

# 这个即为主线程
print id(greenlet.getcurrent()), id(gr1), id(gr2)     # 40239952, 40240272, 40240352

print gr1.switch("hello", " world"), 'back to main'    # hehe back to main