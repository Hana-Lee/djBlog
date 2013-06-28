# -*- coding: utf-8 -*-
from django.http import HttpResponse
from dBlog.models import Article
from django.template import Context, loader

def index(request, page = 1):
    """

    :param request:
    :param page:
    :return: HttpResponse
    """
    page_no = int(page)
    if page_no < 0 :
        page_no = 1

    article_count = Article.objects.all().count()
    if page_no > article_count :
        page_no = 1

    page_title = '블로그 글 목록 화면'

    per_page = 3
    start_pos = (page_no - 1) * per_page
    end_pos = start_pos + per_page

    articles = Article.objects.all().select_related().order_by('-created')[ start_pos : end_pos ]

    tpl = loader.get_template('list.html')
    ctx = Context({
        'page_title' : page_title,
        'articles' : articles,
        'current_page' : page_no
    })
    return HttpResponse(tpl.render(ctx))

def read(request, article_id = None):
    """

    :param request:
    :param article_id:
    :return: HttpResponse
    """
    page_title = '블로그 글 읽기'

    current_article = Article.objects.get(id = int(article_id))
    try:
        prev_article = current_article.get_previous_by_created()
    except:
        prev_article = None

    try :
        next_article = current_article.get_next_by_created()
    except :
        next_article = None

    tpl = loader.get_template('read.html')
    ctx = Context({
        'page_title' : page_title,
        'current_article' : current_article,
        'prev_article' : prev_article,
        'next_article' : next_article
    })

    return HttpResponse(tpl.render(ctx))