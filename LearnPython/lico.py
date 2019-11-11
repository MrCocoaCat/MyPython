# -*- coding: utf-8 -*-
# @Time    : 2019/10/19 18:16
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : lico.py
import fcntl
import threading
import time


def writetoTxt(txtFile):
    id = threading.currentThread().getName()
    with open(txtFile, 'a') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # 加锁
        print("{0} acquire lock".format(id))
        f.write("write from {0} \r\n".format(id))
        time.sleep(3)
    # 在with块外，文件关闭，自动解锁
    #print("{0} exit".format(id))
    time.sleep(4)
    print("{0} exit".format(id))


for i in range(5):
    myThread = threading.Thread(target=writetoTxt, args=("test.txt",))
    myThread.start()

