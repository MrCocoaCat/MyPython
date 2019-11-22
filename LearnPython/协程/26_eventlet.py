# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 10:44
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 26_eventlet.py

import eventlet
import time

eventlet.monkey_patch(thread=False)

urls = [
    "https://www.google.com/intl/en_ALL/images/logo.gif",
    "http://python.org/images/python-logo.gif",
    "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif",
]


def fetch(url):
    print("opening", url)
    time.sleep(2)
    body = [2]
    print("done with", url)
    return url, body


if __name__ == '__main__':
    start = time.time()
    pool = eventlet.GreenPool(8)
    for i in urls:
        pool.spawn_n(fetch, i)
    pool.waitall()

    print(time.time() - start)
