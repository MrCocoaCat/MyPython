import keyword
print(keyword.kwlist)
age1=age2=18
print(age1)
print(age2)
age4,age5,age6=11,12,13

print(age2)
print(age4)
print(age2)

#二进制0b
#八进制0o
#十六进制 0x
text="显示"
age=0x2f
print(text)
print(age)
text2='''sdasdasdasd
sdsdasdasd
asdasdasd'''
print(text2)

#转义字副，利用反斜杠字符
s='Let\'s go'
print(s)
#字符串格式化
#利用%
# %d 此处为整数，%s表示字符串,利用%s符号进行替换
aa='I love %s'
print(aa%'hanmeimei')
#利用format函数
aa="I love {}".format("lilei")
print(aa)
#运算符
print(5/2)
#取整
print(5//2)