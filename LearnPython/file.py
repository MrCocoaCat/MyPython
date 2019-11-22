# -*- coding: utf-8 -*-
# @Time    : 2019/8/20 10:53
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : test.py



import hashlib
import base64
import time
import os
from multiprocessing import Process, Lock
from multiprocessing import Process,Queue,Pool,Manager,Pipe
import sys
import filecmp

def timer(func):
  '''Function Level Timer via Decorator'''
  def timed(*args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    elapse = end - start
    print("Processing time for {} is: {} seconds".format(func.__name__, elapse))
    return result
  return timed


def MD5FileWithName(fineName):
    size = os.path.getsize(fineName)
    #print(size)
    block_size = 512*1024*1024
    #print(block_size)
    i = 0
    with open(fineName, 'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
            i += 1
            print(i, end=' ', flush=True)
        retmd5 = md5.hexdigest()
        return retmd5

def line_MD5FileWithName(fineName):
    size = os.path.getsize(fineName)
    #print(size)
    block_size = 512*1024*1024
    #print(block_size)
    i = 0
    with open(fineName, 'rb') as f:
        md5 = hashlib.md5()
        for fLine in f:
            md5.update(fLine)
        retmd5 = md5.hexdigest()
        return retmd5

def cal_md5(data, li):
    a = time.time()
    md55 = hashlib.md5()
    md55.update(data)
    retmd5 = md55.hexdigest()
    li.append(retmd5)
    print('cal_md5 cost : %s' % (time.time() - a))


def poc_MD5FileWithName(fineName):
    #size = os.path.getsize(fineName)
    #print(size)
    block_size = 512*1024*1024
    #print(block_size)
    i = 0
    md5_list = []
    with open(fineName, 'rb') as f:
        while True:
            data = f.read(block_size)
            cal_md5(data, md5_list)
            #md5_list.append(ret)
            if not data:
                break
            i += 1
            print(i, end=' ', flush=True)
    s = ''.join(sorted(md5_list))
    md56 = hashlib.md5()
    md56.update(s.encode())
    ret = md56.hexdigest()
    return ret


def mul_poc_MD5FileWithName(fineName):
    block_size = 512*1024*1024
    #print(block_size)
    i = 0
    md5_list = Manager().list()
    jobs = []
    with open(fineName, 'rb') as f:
        while True:
            data = f.read(block_size)
            p = Process(target=cal_md5, args=(data, md5_list))
            print(p)
            jobs.append(p)

            if not data:
                break
            i += 1
            print(i, end=' ', flush=True)
    for p in jobs:
        p.start()
        p.join()
    for p in jobs:
        p.join()
    s = ''.join(sorted(md5_list))
    md56 = hashlib.md5()
    md56.update(s.encode())
    ret = md56.hexdigest()
    return ret



def is_file_same(filea,fileb):
    block_size = 1024 * 1024
    fa = open(filea, 'rb')
    fb = open(fileb, 'rb')
    while True:
        data_a = fa.read(block_size)
        date_b = fb.read(block_size)
        if data_a != date_b:
            return False
        if (not data_a) or (not date_b):
            break
    return True

if __name__ == '__main__':
    a = time.time()
    ret = filecmp.cmp('G:\\sss.zip', 'G:\\ssss.zip')
    print(time.time() - a)
    print(ret)


    a = time.time()
    ret = is_file_same('G:\\sss.zip', 'G:\\ssss.zip')
    print(time.time() - a)
    print(ret)

    exit()


    a = is_file_same('G:\\mkv.mkv', 'G:\\sss.zip')
    print(a)
    exit()

    a = time.time()
    md5 = line_MD5FileWithName(fineName='G:\\mkv.mkv')
    print()
    print(time.time() - a)
    print('md5 is %s:' % md5)

    a = time.time()
    md5 = MD5FileWithName(fineName='G:\\mkv.mkv')
    print()
    print(time.time() - a)
    print('md5 is %s:' % md5)

    a = time.time()
    md5 = poc_MD5FileWithName(fineName='G:\\mkv.mkv')
    print()
    print(time.time() - a)
    print('md5 is %s:' % md5)

    # a = time.time()
    # md5 = mul_poc_MD5FileWithName(fineName='G:\\aaaa.zip')
    # print()
    # print(time.time() - a)
    # print('md5 is %s:' % md5)
