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











class RadosThread(threading.Thread):
    def __init__(self, target, args=None):
        self.args = args
        self.target = target
        threading.Thread.__init__(self)

    def run(self):
        self.retval = self.target(*self.args)

# time in seconds between each call to t.join() for child thread
POLL_TIME_INCR = 0.5

def run_in_thread(target, args, timeout=0):
    interrupt = False

    countdown = timeout
    t = RadosThread(target, args)

    # allow the main thread to exit (presumably, avoid a join() on this
    # subthread) before this thread terminates.  This allows SIGINT
    # exit of a blocked call.  See below.
    t.daemon = True

    t.start()
    try:
        # poll for thread exit
        while t.is_alive():
            t.join(POLL_TIME_INCR)
            if timeout and t.is_alive():
                countdown = countdown - POLL_TIME_INCR
                if countdown <= 0:
                    raise KeyboardInterrupt

        t.join()        # in case t exits before reaching the join() above
    except KeyboardInterrupt:
        # ..but allow SIGINT to terminate the waiting.  Note: this
        # relies on the Linux kernel behavior of delivering the signal
        # to the main thread in preference to any subthread (all that's
        # strictly guaranteed is that *some* thread that has the signal
        # unblocked will receive it).  But there doesn't seem to be
        # any interface to create t with SIGINT blocked.
        interrupt = True

    if interrupt:
        t.retval = -errno.EINTR
    return t.retval