def hello(name):
    print("hello {0}".format(name))
    return 1234



ret = hello("world")
print(ret)


def funchengfaviao():
    for row in range(1, 10):
        print("第{0}行 ".format(row), end="")
        for col in range(1, row+1):
            print("{0} * {1} = {2}".format(row, col, col*row), end=' ')
        print(" ")
    return "打印结束"


ret = funchengfaviao()
print(ret)


# 收集参数,参数为tuple类型
# type 检测变量类型
def func(*args):
    print(type(args))
    for ite in args:
        print(ite)
    return None


func(1, "asdad", 3)
# 可以将参数放入list或字典中
ll = ["b", 14]
func(*ll)


# 关键字收集参数，参数为字典类型
def func2(**kwargs):
    '''
     this is 文档
    :param kwargs:
    :return:
    '''
    print(type(kwargs))
    for k, v in kwargs.items():
        print(k, "***   ", v)


func2(name="a ", age=13)
print("\n调用help函数")
help(func2)

print(func2.__doc__)

# eval()函数，将支付串当作一个表达式来执行，返回表达式执行后的结果
# exec()函数无返回值
x = 100
y = 200
z = eval("x+y")
print(z)
