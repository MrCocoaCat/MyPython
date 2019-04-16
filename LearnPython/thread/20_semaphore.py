import threading
import time

semaphore = threading.Semaphore(3)

def func():
    if semaphore.acquire():
        for i in range(5):
            print(threading.current_thread().getName() + " get semaphore")
            time.sleep(2)
            semaphore.release()
            print(threading.current_thread().getName() + " release semaphore")


for i in range(8):
    t1 = threading.Thread(target=func)
    t1.start()
