# -*- coding: utf-8 -*-
# @Time    : 2020/3/1 15:16
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : graph.py
from igraph import *

g = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
print(g)

g.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
g.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
g.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
g.es["is_formal"] = [False, False, True, True, True, False, True, False, False]

print(g.es[0].attributes())
print(g.vs[0].attributes())