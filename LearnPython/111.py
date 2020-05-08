# -*- coding: utf-8 -*-
# @Time    : 2019/8/20 10:53
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : test.py
from requests import put, get,delete,post
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed


import itertools
import multiprocessing
from time import sleep, ctime
from multiprocessing import Process, Lock, Manager
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
from urllib import request
import gevent
from gevent import Greenlet
import gevent,time

from gevent import monkey#打补丁（把下面有可能有IO操作的单独做上标记）
monkey.patch_all()#打补丁

#codebase_list = list(map(chr, range(ord('0'), ord('9') + 1))) + list(map(chr, range(ord('A'), ord('Z') + 1))) + list(map(chr, range(ord('a'), ord('z') + 1)))
codebase_list = list(map(chr, range(ord('a'), ord('z') + 1)))
BASE_URL = 'http://192.168.255.111/practice/login/'
q = queue.Queue()

def gener_passwd(num):
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


def f(url):
    print('GET:%s'%url)
    resp = request.urlopen(url)
    data = resp.read()
    # file = open("data",'wb')#这里可以打开这两步，写入文件
    # file.write(data)
    print('%d bytes received from %s.'%(len(data),url))


#异步模式w
def consur():
    l = []
    while True:
        passwd = q.get()
        a = Greenlet.spawn(do_url, passwd)
        l.append(a)
    gevent.joinall(l)



if __name__ == '__main__':
    async_time_start = time.time()

    p = gevent.spawn(gener_passwd,3)
    c = gevent.spawn(consur)
    gevent.joinall([p, c])


    print("异步步cost", time.time() - async_time_start)



