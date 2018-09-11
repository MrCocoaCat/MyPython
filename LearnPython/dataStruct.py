# 列表
l1 = [1, 2, 3, 6, 7, 10]
print(l1)
print(l1[:])
# 分片左闭右开区间
print(l1[:4])

print(l1[1:4:1])
print(l1[1:4:2])
# 下标可以超出长度，不报错

# 最右侧为-1,默认分片是为左侧到右侧，即左边的值必须小一点
print(l1[-4:-2])

a = 10
b = 10
print(id(a))
print(id(b))

l2 = l1[:]
print(id(l1))
print(id(l2))

# 地址不变，进行原地址删除
print(l2, id(l2))
del l2[1]
print(l2, id(l2))
# 可以对整个链表进行删除
del l2

# 链表相加
a = [1, 2, 3]
b = [4, 6, 8]
c = a + b
print(c)

# 列表内涵
e = [i*10 for i in c]
print(e)

e = [i*10 for i in c if i % 2 == 0]
print(e)
# 列表相乘则表示多个相接
d = 5 * a
print(d)
# in 判断一个元素是否包含在一个列表中，返回一个布尔值
print(3 in d)

# 特别注意,嵌套的链表可以直接打印，这时候必须每个子链表都相同
ll = [[1, 10], [2, 20], [3, 30]]
for a, b in ll:
    print(a, b)

# 列表的函数
print(len(d))
# max()求列表中的最大值,可以比较字母
l5 = ["a", "c", "b"]
print(max(l5))

# 转换为列表
s = "asdadfagafgatgr"
print(list(s))

# 复杂变量传地址，简单变量传值
ll = [1, 2, 3, 4]
ll.append(100)
print(ll)
ll.insert(3,300)
print(ll)
# 把最后一个元素删除
ll.pop()
print(ll)
# 删除指定的元素,在原链表进行操作
ll.remove(2)
# 清空列表
ll.clear()
# 反转列表，直接对原地址进行操作,extend是扩展
lv = [1, 2, 3]
lv.reverse()
print(lv)
# count 查找列表中元素个数
print(list(s))


#

# 复杂变量传地址，简单变量传值
i = lv.count(2)
print(i)
# 利用 = 赋值是进行，直接指向统一快空间
a = [1, 2, 3]
b = a
# 二者的id 相同
print(id(a))
print(id(b))
a.append(5)
print(b)

# 利用copy函数是浅拷贝，只复制一层
c = a.copy()
a.append(8)
# c与a 的不相同
print("a: ", a, id(a))
print("c: ", c, id(c))


# 元组tuple,可以看成是一个不可改变的list
# 有序，元组可以是任意类型。总之list所有特性，除了修改元祖都有
t = (1, 2)
print(type(t))
# 可以不带括号进行使用
tt = 1, 2, 3, 4, 5
print(type(tt))

# 不可修改是指其元素不可修改
for i in tt:
    print(i, end=" ")



print(type(t))

print(a)
tt = tuple(a)
print(tt)

# set集合,数据唯一,并且自动排序
s = {9, 1, 2, 3, 5, 1}
print(s)
# 集合内涵

ss = {i for i in s if i % 2 == 0}
print(ss)

# add 向集合中添加元素, pop是随机删除
ss.add(1010)
print(ss)

# frozen set 冰冻集合


# 字典dict, key:value
d = {"one": 1, "twe": 2, "three": 3}
print(d)

print(d["one"])
# 遍历字典
for k in d.keys():
    print(k, d[k], end=" ")

for v in d.values():
    print(v, end=" ")

for k, v in d.items():
    print(k, "---", v, end=" ")

