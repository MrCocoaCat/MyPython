# -*- coding: utf-8 -*-
# @Time    : 2020/2/7 21:15
# @Author  : MrCocoaCat
# @Email   : MrCocoaCat@aliyun.com
# @File    : 1.py

from urllib import request
import chardet

if __name__ == '__main__':

    url = "https://study.163.com/course/courseLearn.htm?courseId=1004987028#/learn/video?lessonId=1052092284&courseId=1004987028"
    res = request.urlopen(url)

    print("url: %s" % res.geturl())
    print(res.info())
    print(res.getcode())

    #print(res)
    html = res.read()
   # print(html)
    cs = chardet.detect(html)
    print(cs)
    css = cs.get("encoding", "utf-8")
    # 解码
    print(html.decode(css))


