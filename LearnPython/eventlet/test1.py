# -*- coding: utf-8 -*-
# @Time    : 2019/1/29 11:01
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : test1.py

import eventlet.event
import eventlet.queue
import eventlet.semaphore
import eventlet.wsgi
import time


def _launch(*args, **kwargs):
    ret = args[0]**3
    time.sleep(2)
    print ret


def _launchb(*args, **kwargs):
    ret = args[0]**4
    time.sleep(1)
    print ret


if __name__ == '__main__':
    time_begin = time.time()
    list1 = []
    list2 = []
    for i in range(0, 5):
        thr = eventlet.spawn(_launch, i)
        print thr
        thr2 = eventlet.spawn(_launchb, i)
        print thr2
        list1.append(thr)
        list1.append(thr2)
        #list2.append(thr2)

    for thr1 in list1:
        thr1.wait()
    for thr2 in list2:
        thr2.wait()
    print time.time() - time_begin

