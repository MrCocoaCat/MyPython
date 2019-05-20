from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def book(request):
    return HttpResponse('图书首页')


def book_detail(request, book_id):
    text = "book id is %s" % book_id
    return HttpResponse(text)


def author_detail(request):
    author_id = request.GET.get('id')
    text = "作者id 为 %s" % author_id
    return  HttpResponse(text)