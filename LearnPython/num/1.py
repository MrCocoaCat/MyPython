# -*- coding: utf-8 -*-
# @Time    : 2020/3/3 17:56
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 1.py


import numpy as np

# a = np.array([[1,  2],  [3,  4]])

b = np.array([[0,1,1,0,0],
             [1,0,0,1,0],
             [1,0,0,0,1],
             [0,1,0,0,0],
             [0,0,1,0,0]])
# print(b)
# print(b.ndim)
# print(b.shape)
n,m = b.shape

print(n)
print(m)

bh = 1
for i in range(m):
    for j in range(n):
        if b[i][j] == 1:
            b[i][j] = bh
            bh = bh + 1
        #print(b[i][j])

print(b)

# c = np.transpose(b)
c = b.T
print(c)


print(20 * '*')
b2 = [str(x) for x in b.flat]
c2 = [str(x) for x in c.flat]
print(b2)
print(c2)




