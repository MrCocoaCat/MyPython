# encoding:utf-8
from flask import Flask,url_for
# import config
app = Flask(__name__)


# 如果浏览器要访问服务器程序的根地址（"/"），
# 那么 Flask 程序实例就会执行函数 hello()，返回『Hello World!』。
@app.route("/")
# 这个是一个装饰器，url与是凸函数的映射
def hello():
	print url_for('my_list')
	print url_for('article', id='abc')
	return "hello world"


# 传参数
@app.route("/article/<id>")
def article(id):
	return "ufff %s" %id


@app.route("/list/")
def my_list():
	return 'list'


if __name__ == '__main__':
	# 读取配置文件
	# app.config.from_object(config)
	# 开启debug 模式，
	app.run(debug=True)
