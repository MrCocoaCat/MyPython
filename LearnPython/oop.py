# 定义一个空类
class Student():
    pass


class PythonStudent():
    name = None
    age = 18
    # self 相当于 this 函数

    def myfun(self):
        print("do homework")
        self.age = 23
        return None


wang = PythonStudent()
print(wang.age)
print(PythonStudent.__dict__)
print(" ")
# 创建对象的时候内部无成员
print(wang.__dict__)

# 赋值的时候有相应成员
wang.age = 19
print(wang.__dict__)

wang.myfun()
print(wang.age)

# self 表示对象本身 ，其为函数的第一个参数，将对象作为第一个参数进行传入
# 其并不是一个关键字

class Teacher():
    name = "nina"

    def sayhello(selff):
        selff.name = "ffffff"
        print("HELLO {0}".format(selff.name))

    def sayAgain():
        print("jjjjj")


nnn = Teacher()
nnn.sayhello()
# 仅当其为对象时才会自动被传入
Teacher.sayAgain()

class A():

    name = "liu"
    age = 18

    def __init__(self):
        self.age = 19
        self.name = "zhang"

    def say(self):
        print("*"*20)
        print(self.name)
        print(self.age)


class B():
    name = "liuuuuu"
    age = 18888


a = A()
a.say()
#　此时，self被a 替换
A.say(a)
# 同样，可以将A传入
A.say(A)

# 鸭子类型
A.say(B)
