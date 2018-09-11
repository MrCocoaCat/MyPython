# 封装，多态
class A():
    name = "ttttt"
    # 前面加＂__＂就是私有成员
    __age = 18

    def __init__(self):
        self.name = "aaa"

a = A()
# 不可以访问，其为私有变量
# 其为假私有，只是改名字存储

# print(a.age),会出错
# 通过更改名字可以进行访问
print(a._A__age)
#　封装，对成员对象进行封装
#  公开　public
#  保护　protected
#  私有　private　

# 继承
class Person():
    name = "Noname"
    age = 0
    __score = 20  # 私有
    _petname = "xiaohua"  # 保护

    def sleep(self):
        print("ummmmm")

    def work(self):
        print("make money,I'm {0}".format(self.name))


class Teacher(Person):
    name = "Nina"

    def make_test(self):
        print("attention, testing ")

    def work(self):
        # 调用父类的函数
        Person.work(self)
        # 也可以用super调用父类方法
        super().work()
        self.make_test()

# 所有的类都继承于Object
# 其可以使用除私有成员之外的所有成员

# 如子类与父类的函数相同，则调用子类函数


T = Teacher()
print(T.name)
print(T.age)
# 通过引用使用，并没有进行拷贝
print(id(T.name))
print(id(Person.name))

T.sleep()
T.work()

print("*" * 30)
# 构造函数若此类中没有，则查找父类的


class Animal():
    def __init__(self):
        print("init animal      ")


class Bulu(Animal):
    def __init__(self, name):
        print("Init bulu {0}".format(name))


class Dog(Bulu):
    def __init__(self):
        print("init dog")


class Cat(Bulu):
    pass


d = Dog()
# 无构造则找父类构造

# c = Cat(), 会报错，缺参数
c = Cat("dsdf")

# super 不是一个关键字，而是一个类
# 其作用为获取MRO， 及列表中的第一个类



