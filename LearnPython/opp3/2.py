# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 20:48
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 2.py


class Point:
    def __init__(self):
        pass

    def __str__(self):
        return 'Point is (%s,%s)' %(self.x, self.y)

    def __setitem__(self, key, value):
        print('Called the __setitem__ function')
        self.__dict__[key] = value

    def __getitem__(self, item):
        print('Called the __getitem__ function')
        try:
            if item == 'x':
                return '%s' % self.x
            elif item == 'y':
                return '%s' % self.y
        except:
            return 'There is no this item in class Point'

    def __delitem__(self, key):
        del self.__dict__[key]


if __name__ == '__main__':
    p = Point()
    p['x'] = 3
    print(p.__dict__)
    print(p['x'])
    #
    p['y'] = 6
    print(p)
    del p['x']
    print(p['x'])