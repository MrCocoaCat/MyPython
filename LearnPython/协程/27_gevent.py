import gevent, time
from gevent import monkey
import eventlet



monkey.patch_all()  # gevent三行放在其他所有import语句之前可以避免出现警告或者报错信息,导致程序不能正常运行


def test1():
    for i in range(10):
        time.sleep(1)
        print('test1', 1)


def test2():
    for i in range(10):
        time.sleep(2)
        print('test2', 2)


g1 = gevent.spawn(test1)
g2 = gevent.spawn(test2)
g1.join()
g2.join()