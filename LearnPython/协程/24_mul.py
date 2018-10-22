# yield 返回
# send 调用

def simple_C():
    print('-> start')
    x = yield
    print("-> revived",x)

# 主线程
sc = simple_C()
print(111)
# 预计
next(sc)
#
print(222)
# 将值发给x
sc.send("sdsdf")


print(10 * '*')