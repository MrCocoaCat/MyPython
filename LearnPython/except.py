
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

#os.path
# abspath()将路径装环卫绝对路径
# join() 将多个路径组合成一个路径

import os.path as op
# 将路径进行拆分，拆分为文件名和路径
#t = op.split("/home/liyubo/test.md")
#print(t)

# isdir() 判断其是否为一个目录
# exists() 判断文件是否存在

# shutil 模块
# shutil.copy(原路径，目标路径)
# copy2 尽可能保留文件信息
# move(源路径，目标路径)

# 归档和压缩
# make_archive(归档后的目录和文件名，后缀，需要归档的文件夹)
# make_unpack_archive 反归档
import shutil
#shutil.make_archive()

# 压缩文件
import zipfile
# 压缩
#zf = zipfile.ZipFile("./test")
# 解压 extractall

# 随机数
import random
# 生成0-1 的随机小数
print(random.random())

l1 = [i for i in range(10)]
print(l1)

# 打乱排序
random.shuffle(l1)
print(l1)

# 随机生成[0，100]的随机数
print(random.randint(0, 100))