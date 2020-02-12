import time, re
import os, datetime
from concurrent import futures

data = range(20)


def wait_on(argument):
   print(argument)
   a = 0
   for j in range(argument):
      for i in range(100000):
            a = a + i
   print a
   return "ok"


ex = futures.ThreadPoolExecutor(max_workers=2)
for i in data:
   ex.submit(wait_on, i)
# for i in ex.map(wait_on, data):
#    print(i)
# time.sleep(1)