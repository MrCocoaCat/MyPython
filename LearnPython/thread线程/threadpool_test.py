# -*- coding: utf-8 -*-
# @Time    : 2020/3/10 20:42
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : threadpool_test.py


from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_EXCEPTION
import time


def work(num):
    a = num
    # while True:
    #     a = a + 1
    #     a = a - 1
    time.sleep(5)
    print("times is %s " % num)
    return num


executor = ThreadPoolExecutor(max_workers=2)
# 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞

task = executor.submit(work, 3)
# done方法用于判定某个任务是否完成
print("task done is : %s " % task.done())
# cancel方法用于取消某个任务,该任务没有放入线程池中才能取消成功
print(task.cancel())

# 标记为已完成并设置结果.
# task.set_result(1000)
print("running : %s "% task.running())
# 标记为已完成并设置例外.
task.set_exception(Exception("errot -----"))

print("task done is : %s " % task.done())
# result方法可以获取task的执行结果
print("result is :%s" % task.result())

wait([task], return_when=ALL_COMPLETED)
executor.shutdown()
