def simple_coroutine(a):
    print('-> start ')
    b = yield a
    # 接到返回值时继续运行
    print('-> receve',a,b)
    print('-> receve',a,b)
    c = yield a+b
    print("-> reveve",a,b,c)
    print("-> reveve",a,b,c)

sc = simple_coroutine(5)

# 当yield 时触发,执行之send结束，即send 返回值
aa = next(sc)
print(aa)
print(aa)
bb = sc.send(6)

print(bb)
print(bb)
cc =  sc.send(7)
print(cc)
