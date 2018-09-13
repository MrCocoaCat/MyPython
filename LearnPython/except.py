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


