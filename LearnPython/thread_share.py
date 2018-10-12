#共享变量

import threading

mySum = 0
loop = 1000


def my_add():
    global  mySum,loop
    for i in range(1, loop):
        mySum += 1

def my_del():
    global  mySum,loop
    for i in range(1, loop):
        mySum -= 1

if __name__=='__main__':
    print("starting ...{0}".format(mySum))

    t1 = threading.Thread(target=my_add,args=())
    t1.start()

    t2 = threading.Thread(target=my_del(), args=())
    t2.start()

    t1.join()
    t2.join()
    print("all thread finish，sum is {0}".format(mySum))