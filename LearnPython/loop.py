age = input("please input age")
# input 是字符串类型，需要强制转换
age = int(age)
if age < 18:
    print("未成年")
else:
    print("成年")
# 列表
for name in ['zs', 'ls', 'wer']:
    print(name)
    if name == 'zs':
        print("张三")
# range 生成一个数字序列,左闭右开区间

for i in range(1, 10):
    pass
    print(i)
else:
    print("退出循环")

money = 1000
year = 0
while money < 2000:
    money = money*1.1
    year += 1
    print("第 {0} 年拿了 {1} 钱)".format(year,money))

