# 模块，增加程序复用，
# 避免命名冲突
# 函数（单一功能）
# 类（相似的功能的组合）
# 测试代码

# 语法 import * as * 别名
#

# 作为程序入口,作为包调用时，并不执行
# 可以有效的解决被动执行的问题


import sys
sys.path

mydir = "/n/dfdf"
# 添加自己的搜索路径
sys.path.append(mydir)

# 收索内存中已经加载好的模块
# 所搜内置模块
# 搜索sys.path



if __name__ == '__main__':
    print("aaaaa")

# 包，为一个软件结构
# 其中包含一个—__init.py 文件
# import package_name 导入包
# import package_name as nn 仅导入init 文件

