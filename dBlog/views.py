# -*- coding: utf-8 -*-
from django.http import HttpResponse
from dBlog.models import Article
from django.template import Context, loader

def index(request, page = 1):
    page = int(page)
    page_title = '블로그 글 목록 화면'

    per_page = 3
    start_pos = (page - 1) * per_page
    end_pos = start_pos + per_page

    articles = Article.objects.all().order_by('-created')[ start_pos : end_pos ]

    tpl = loader.get_template('list.html')
    ctx = Context({
        'page_title' : page_title,
        'articles' : articles,
        'current_page' : page
    })
    return HttpResponse(tpl.render(ctx))

def read(request, article_id = None):
    page_title = '블로그 글 읽기'

    current_article = Article.objects.get(id = int(article_id))

    return HttpResponse('[%s]번째 글입니다. 제목 : [%s]' % (current_article.id, current_article.title.encode('utf-8')))