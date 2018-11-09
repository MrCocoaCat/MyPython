import multiprocessing
from time import sleep,ctime
import os

class ClockProcess(multiprocessing.Process):

    def __init__(self,interval):
        super().__init__()
        self.interval = interval

    def run(self):
         while True:
            print("The time is %s" % ctime())
            print(os.getpid())
            print(os.getppid())
            sleep(self.interval)


if __name__=='__main__':
    p= ClockProcess(3)
    print(os.getpid())
    p.start()
    p.join()

