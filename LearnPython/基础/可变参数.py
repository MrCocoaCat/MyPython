# -*- coding: utf-8 -*-
# *args表示任何多个无名参数，它是一个tuple；
# **kwargs表示关键字参数，它是一个 dict。
# 并且同时使用*args和**kwargs时，*args参数列必须要在**kwargs前，
# 像foo(a=1, b='2', c=3, a', 1, None, )这样调用的话，会提示语法错误


def foo(name, *args, **kwargs):
    print(name)
    print(args)
    print(kwargs)
    print('-----------------------')


if __name__ == '__main__':
    foo(100)
    foo(1, 2, 3, 4)
    foo(100, a=1, b=2, c=3)
    foo(1, 2, 3, 4, a=1, b=2, c=3)
    foo('a', 1, None, a=1, b='2', c=3)
