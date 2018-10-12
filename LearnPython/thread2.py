import time
import _thread as thread

def loop1(in1):
    print("start loop1 at ",time.ctime())
    print("par ",in1)
    time.sleep(4)
    print("end loop1 at ",time.ctime())


def loop2(in1,in2):
    print("start loop2",time.ctime())
    print("par 1", in1,"par 2", in2 )
    time.sleep(2)
    print("end loop2",time.ctime())


def main():
    print("start at",time.ctime())
    print("start at")
    print(time.ctime())
    thread.start_new_thread(loop1, ("a",))
    thread.start_new_thread(loop2, ("b", "c"))

    print("all enf",time.ctime())


if __name__ == '__main__':
    print("begin")
    main()


