import time
import _thread as thread

def loop1(in1):
    print("start loop1 at ",time.ctime())
    print("参数",in1)
    time.sleep(4)
    print("end loop1 at ",time.ctime())


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


