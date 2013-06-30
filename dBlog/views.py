# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from dBlog.models import Article
from django.template import Context, loader, RequestContext


def index(request, page=1):
    page_no = int(page)
    if page_no < 0:
        page_no = 1

    article_count = Article.objects.all().count()
    if page_no > article_count:
        page_no = 1

    page_title = '블로그 글 목록 화면'

    per_page = 3
    start_pos = (page_no - 1) * per_page
    end_pos = start_pos + per_page

    articles = Article.objects.all().select_related().order_by('-created')[start_pos: end_pos]

    tpl = loader.get_template('list.html')
    ctx = Context({
        'page_title': page_title,
        'articles': articles,
        'current_page': page_no
    })
    return HttpResponse(tpl.render(ctx))


def read(request, article_id=None):
    page_title = '블로그 글 읽기'

    current_article = Article.objects.get(id=int(article_id))
    try:
        prev_article = current_article.get_previous_by_created()
    except:
        prev_article = None

    try:
        next_article = current_article.get_next_by_created()
    except:
        next_article = None

    tpl = loader.get_template('read.html')
    ctx = Context({
        'page_title': page_title,
        'current_article': current_article,
        'prev_article': prev_article,
        'next_article': next_article
    })

    return HttpResponse(tpl.render(ctx))


def write_form(request):
    page_title = '블로그 글 쓰기'
    data_dict = ({'page_title': page_title})
    return render_to_response('write.html', data_dict, context_instance=RequestContext(request))


def add_post(request):
    formAva = checkWriteForm(request)

    if formAva == False:
        return HttpResponse('필수값 입력 여부를 확인하세요')

    article_title = request.POST['title']
    return HttpResponse('hello %s' % article_title)


def checkWriteForm(request):
    if request.POST.has_key('title') == False:
        return False
    elif request.POST.has_key('content') == False:
        return False

    if len(request.POST['title']) == 0:
        return False

    if len(request.POST['content']) == 0:
        return False

    return True