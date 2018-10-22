import multiprocessing
from time import ctime

#生成器
#yeild 负责返回
def odd():
    print("step 1")
    yield 1
    print("step 2")
    yield 2
    print("step 3")
    yield 3

# odd() 是调用生成器
g = odd()
one = next(g)
print(one)

two = next(g)
print(two)


print(10*'*')
def fib(max):
    n,a,b = 0, 0, 1
    while n < max:
        print(b)
        a,b=b,a+b
        n+=1
    return "done"

fib(5)


print(20*'*')
# 生成器的yield负责返回值

def fibb(max):
    n,a,b = 0, 0, 1
    while n < max:
        yield b
        a,b = b,a+b
        n+=1
    return "done"

# 调用生成器
g = fibb(5)
for i in range(5):
    rst = next(g)
    print(rst)