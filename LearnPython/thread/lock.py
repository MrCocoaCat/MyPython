import fcntl
import threading
import time


def writetoTxt(txtFile):
    id = threading.currentThread().getName()
    with open(txtFile, 'a') as f:
        print(f.fileno())
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        print( "{0} acquire lock".format(id))
        f.write("write from {0} \r\n".format(id))
        time.sleep(3)
    print( "{0} exit".format(id))


for i in range(5):
    myThread = threading.Thread(target=writetoTxt, args=("test.txt",))
    myThread.start()
