

def now():
    print('2013-12-25')


# 在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）
def log(func):
    def wrapper(*args, **kw):
        print("this is log,call {0}".format(func.__name__))
        return func(*args, **kw)
    return wrapper


@log
def fun():
    print('this is fun')


if __name__ == '__main__':
    # 函数对象可以估值给变量
    f = now
    f()
    print('*'*20)
    fun()


