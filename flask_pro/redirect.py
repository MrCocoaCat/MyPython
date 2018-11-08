# encoding:utf-8
from flask import Flask,url_for,redirect
# import config

app = Flask(__name__)


@app.route("/")
def index():
	print "this is frist page"
	login_url = url_for('login')
	return redirect(login_url)


@app.route("/login/")
def login():
	return "this is login page"


@app.route("/question/<is_login>")
def question(is_login):
	if is_login == '1':
		return "this is question page"
	else:
		return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(debug=True)
