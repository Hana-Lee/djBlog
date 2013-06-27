# -*- coding: utf-8 -*-
from django.http import HttpResponse
from dBlog.models import Article

def index(request, page=1):
    page_title = '블로그 글 목록 화면'
    articles = Article.objects.all()
    return HttpResponse('안녕? 이곳은 [%s] 입니다.' % page_title)