
try:
    num = 0
    ret = 100/num
    print("结果为{}".format(ret))

except ZeroDivisionError as e:
    print(e)


#自定义一个异常,继承ValueError

class DanaError(ValueError):
    pass


try:
    print("test")
    # 手动引发异常
    raise DanaError
except NameError as e:
    print("NameError")
except ValueError as e:
    print("ValueError")
finally:
    print("最后执行")

# 自定义异常，方便扩展


# 日历模块
import calendar
cal = calendar.calendar(2017)
print(cal)

# time 模块 1970年
# UTC时间，国际标准时间
import time

# 与标准时间的时间差
print(time.timezone)

# 获取时间戳
print(time.time())

# sleep 1 秒
time.sleep(1)


import datetime

print(datetime.date(2018, 3,26))

import os

# 获取当前文件目录
mydir = os.getcwd()
print(mydir)

# chdir()改变当前工作目录
ld = os.listdir()
print(ld)

# 递归创建文件夹
#rst = os.makedirs("test")


# 执行系统命令
# 可使用subprocess进行代替
rst = os.system("ls")

# 获取环境变量
rst = os.getenv("PATH")
print(rst)

print(os.pardir)
print(os.curdir)

