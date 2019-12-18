from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED
import time
from queue import Queue
import threading

queue = Queue()
lock = threading.Lock()
x = 0


def return_future(msg):
    if not queue.empty():
        num = queue.get()
        print(num)
        time.sleep(0.1)
        # queue.put(num)
    else:
        print("empty")
        #print("size %s" % queue.qsize())
        lock.acquire()
        global x
        x += 2
        print("x %s " % x)
        for j in range(x-2, x):
            queue.put(j)
        lock.release()
        num = queue.get()
        print(num)
    return msg


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=5)
    all_task = [pool.submit(return_future, i) for i in range(2000)]
    # print(all_task)
    wait(all_task, return_when=ALL_COMPLETED)


