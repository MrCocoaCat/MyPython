# -*- coding: utf-8 -*-
# @Time    : 2019/1/9 10:04
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 4.py

from greenlet import greenlet
def test1():
    gr2.switch(1)
    print 'test1 finished'

def test2(x):
    print 'test2 first', x
    z = gr1.switch()
    print 'test2 back', z

gr1 = greenlet(test1)
gr2 = greenlet(test2)
# 启动协程1
gr1.switch()

# dead 属性查看是否结束
print 'gr1 is dead?: %s, gr2 is dead?: %s' % (gr1.dead, gr2.dead)

# 启动协程2
gr2.switch()
print 'gr1 is dead?: %s, gr2 is dead?: %s' % (gr1.dead, gr2.dead)
print gr2.switch(10)