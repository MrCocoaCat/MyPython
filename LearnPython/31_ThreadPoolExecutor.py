from concurrent.futures import ThreadPoolExecutor
import time

def return_future(msg):
    time.sleep(3)
    return msg

pool = ThreadPoolExecutor(max_workers=2)

f1 = pool.submit(return_future,'hello1')
f2 = pool.submit(return_future,'hello2')

# 等待执行完毕
print(f1.done())
print(f2.done())

# 结果
print(f1.result())
print(f2.result())
