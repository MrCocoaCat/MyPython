# coding=utf8
# start_response()函数接收两个参数，
# 一是HTTP响应码，
# 二是一组list表示的HTTP Header，每个Header用一个包含两个str的tuple表示。
# Content-Type指示响应的内容，这里是text/html表示HTML网页


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']