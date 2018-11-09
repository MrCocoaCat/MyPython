import time
import _thread as thread

def loop1():
    print("start loop1",time.ctime())
    time.sleep(4)
    print("end loop1",time.ctime())


def loop2():
    print("start loop2",time.ctime())
    time.sleep(2)
    print("end loop2",time.ctime())


def main():
    print("start at",time.ctime())
    thread.start_new_thread(loop1, ())
    thread.start_new_thread(loop2, ())


    print("all enf",time.ctime())


if __name__ == '__main__':
    print("begin")
    main()


