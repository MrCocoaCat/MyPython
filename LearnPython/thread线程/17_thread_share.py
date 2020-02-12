#共享变量

import threading

mySum = 0
lock = threading.Lock()

def my_add():
    global  mySum
    for i in range(0 , 100000):
        lock.acquire()
        mySum += 1
        lock.release()

def my_del():
    global  mySum
    print("starting del")
    for i in range(0, 100000):
        lock.acquire()
        mySum -= 1
        lock.release()

if __name__=='__main__':
    print("starting ...{0}".format(mySum))

    t1 = threading.Thread(target=my_add,args=())
    t1.start()

    t2 = threading.Thread(target=my_add, args=())
    t2.start()

    t3 = threading.Thread(target=my_del, args=())
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print("all thread finish，sum is {0}".format(mySum))

    # 线程安全数据类型 queue
    