# -*- coding: utf-8 -*-
# @Time    : 2020/3/10 21:22
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : threadpool_test2.py


import queue
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED, FIRST_EXCEPTION


def send_cmd(ip, exec_queue):
    # 如果消息队列中消息不为空，说明已经有任务异常了
    if not exec_queue.empty():
        return
    try:
        # 需要执行的主任务
        print(ip)
    except Exception as e:
        # 如果任务异常了就在队列中写入一个消息，用于锁住线程池
        exec_queue.put("Termination")
        # 此处一定要将异常再次抛出，否则主线程池无法捕获异常，会统一认定为任务已被取消
        raise Exception(e)


# 此处使用消息队列作为线程池锁，避免在第一个任务异常发生后到主线程获知中间仍然有任务被发送执行
exec_queue = queue.Queue()
with ThreadPoolExecutor(max_workers=5) as executor:
    task_dict, task_list = {}, []
    # 将任务全部放入线程池中
    for ip in ["aaa","bbb"]:
        task = executor.submit(send_cmd, ip, exec_queue)
        task_dict[task] = ip
        task_list.append(task)
    # 等待第一个任务抛出异常，就阻塞线程池
    wait(task_list, return_when=FIRST_EXCEPTION)
    # 反向序列化之前塞入的任务队列，并逐个取消
    for task in reversed(task_list):
        task.cancel()
    # 等待正在执行任务执行完成
    wait(task_list, return_when=ALL_COMPLETED)

    for task in task_list:
        if task_dict.get(task):
            if "finished returned NoneType" in str(task) or task.cancelled():
                print("{}被取消".format(task_dict.get(task)))
            elif "finished raised Exception" in str(task):
                print("{}执行异常".format(task_dict.get(task)))
            else:
                print("{}执行成功".format(task_dict.get(task)))
