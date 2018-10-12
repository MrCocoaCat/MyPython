import threading
import time

class MyThread(threading.Thread):
    def __init__(self, arg):
        super(MyThread, self).__init__()
        self.arg = arg

    def run(self):
        time.sleep(2)
        print("arg is ".format(self.arg))

def main():
    for i in range(5):
        t = MyThread(i)
        t.start()
        t.join()

if __name__ == '__main__':
    main()