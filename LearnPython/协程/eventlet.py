# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 10:44
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : eventlet.py


import time

import eventlet


def test(s):
    print(s)
    time.sleep(1)


pool = eventlet.GreenPool()
# for i in range(3):
#     pass
