try :
    num = int(input("please input your number： "))
    ret = 100/num
    print("结果为{}".format(ret))

except ZeroDivisionError as e:
    print(e)

