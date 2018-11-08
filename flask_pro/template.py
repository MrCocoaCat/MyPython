# encoding: utf-8
from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def index():
    class person(object):
        name = u"汤唯"
        age = 28
    p = person()
    context = {
        'username': u'冰冰',
        'age': 20,
        'person': p
    }
    return render_template('index.html', **context)


@app.route('/login/<is_login>/')
def login(is_login):
    if is_login == '1':
        user = {
            'username': u'李建',
            'age': 18
        }
        return render_template('login.html', user=user)
    else:
        return render_template('login.html')


@app.route('/for/')
def index2():
    user = {
        'username': u'灯槽',
        'age': 18
    }
    return render_template('indexfor.html', user=user)


@app.route('/image/')
def filter():

    return render_template('filter.html'
                           #,avatar='http://192.168.125.123/dashboard/static/dashboard/img/logo.svg'
                           )


if __name__ == '__main__':
    app.run(debug=True)
