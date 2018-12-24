# encoding:utf-8
from flask import Flask

app = Flask(__name__)
# @其为一个装饰器
# url 与视图函数的映射
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
