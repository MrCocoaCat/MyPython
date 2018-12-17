import threading
import time
import queue

class Producer(threading.Thread):
    def run(self):
        global queue
        count = 0
        while True:
            if queue.qsize() < 1000:
                for i in range(100):
                    count = count + 1
                    msg = "pro" + str(count)
                    queue.put(msg)
                    print(msg)
            time.sleep(0.5)

class Consumer(threading.Thread):
    def run(self):
        global queue
        while True:
            if queue.qsize() > 100:
                for i in range(3):
                    msg = self.name + "consum" + queue.get()
                    print(msg)
            time.sleep(1)

if __name__=='__main':
    quene = queue.Quene()

    for i in range(500):
        queue.put("初始产品 "+ str(i))
    for i in range(2):
        p = Producer()
        p.start()

    for i in range(2):
        c = Consumer()
        c.start()