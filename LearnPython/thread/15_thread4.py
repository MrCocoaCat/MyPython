import time
import threading

def loop1(in1):
    print("start loop1 at ",time.ctime())
    print("par: ",in1)
    time.sleep(4)
    print("end loop1 at ",time.ctime())


def loop2(in1,in2):
    print("start loop2",time.ctime())
    print("par 1:  ", in1,"par 2:  ", in2 )
    time.sleep(2)
    print("end loop2",time.ctime())


def main():
    print("start at",time.ctime())

    t1 = threading.Thread(target=loop1, args=("a",))
    # 守护线程，在主线程结束时自动结束运行
    t1.setDaemon(True)
    # 设置线程名称
    t1.setName("TH1")
    t1.start()

    t2 = threading.Thread(target=loop2, args=("b", "c"))
    t2.start()
    t2.setName("TH2")

    #现在运行的所有线程 enumerate()
    for thr in threading.enumerate():
        print(thr.getName())


    t1.join()
    t2.join()



    print("all end at",time.ctime())


if __name__ == '__main__':
    print("begin")
    main()


