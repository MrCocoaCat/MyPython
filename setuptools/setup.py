#-*- encoding: UTF-8 -*-

from setuptools import setup

setup(
    name = "demo",                # 包名
    version = "0.1",              # 版本信息
    packages = ['demo'],          # 要打包的项目文件夹
    include_package_data=True,    # 自动打包文件夹内所有数据
    zip_safe=True,                # 设定项目包为安全，不用每次都检测其安全性
    install_requires = [          # 安装依赖的其他包（测试数据）
    'docutils>=0.3',
    'requests',
    ],

    # 设置程序的入口为path
    # 安装后，命令行执行path相当于调用get_path.py中的fun方法
    entry_points={
        'console_scripts':[
            'path = demo.get_path:fun'
                                      ]
    },

)
