# -*- coding: utf-8 -*-
# @Time    : 2019/12/18 10:19
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : proporty.py


class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2019 - self._birth


a = Student()
a.birth = 1991
print(a.age)
a.age=100