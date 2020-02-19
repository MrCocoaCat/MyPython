# -*- coding: utf-8 -*-
# @Time    : 2020/2/14 21:30
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : c2.py
import stomp
from MQ.listen import MyListener
from queue import Queue
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import random


def listen_from_MQ(queue):
    conn = stomp.Connection([('192.168.83.132', 61613)])
    conn.set_listener('2', MyListener(con=conn, queue=queue,))
    conn.connect('admin', 'password', wait=True)
    try:
        conn.subscribe(destination='test1', id="c2", ack='client-individual')
        while True:
            pass
    except Exception():
        conn.unsubscribe("1")
        conn.disconnect()


def con_fun(a):
    print("begin do :%s " % a)
    time.sleep(random.randint(3, 15))
    print(" done :%s " % a)


def consumer(queue):
    pool = ThreadPoolExecutor(max_workers=5)
    message_thread_dic = {}
    while True:
        a = queue.get()
        print("consumer : %s" % a)
        if int(a) % 10 == 0:
            b = str(int(a)-3)
            thread_q = message_thread_dic.setdefault(b, None)
            if thread_q:
                print("%s is %s" % (thread_q, thread_q.done()))
        else:
            thread_id = pool.submit(con_fun, a)
            message_thread_dic[a] = thread_id


        # print(all_task)
        #wait(all_task, return_when=ALL_COMPLETED)


if __name__ == '__main__':
    queue = Queue()
    thread1 = threading.Thread(target=listen_from_MQ, args=(queue,))
    thread1.setDaemon(True)
    thread1.start()
    thread2 = threading.Thread(target=consumer, args=(queue,))
    thread2.setDaemon(True)
    thread2.start()
    thread1.join()