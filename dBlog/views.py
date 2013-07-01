# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext
from django.db import transaction

from dBlog.models import Article, Category, Tag


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
    categories = Category.objects.all()

    data_dict = ({
                     'page_title': page_title,
                     'categories': categories
                 })
    return render_to_response('write.html', data_dict, context_instance=RequestContext(request))


def add_post(request):
    """

    :param request:
    :return:
    """
    formAva = checkWriteForm(request)

    if formAva is False:
        return HttpResponse('필수값 입력 여부를 확인하세요')

    try:
        article_category = Category.objects.get(id=request.POST.get('category'))
    except:
        return HttpResponse('헐....카테고리 지정안되어있음.')

    tag_list = []
    if request.POST.has_key('tags') is True:
        #split_tags = unicode(request.POST.get('tags')).split(',')

        #for tag in split_tags:
        #    tag_list.append(tag.strip())
        tags = map(lambda str: str.strip(), unicode(request.POST.get('tags')).split(','))
        tag_list = updateTag(tags)

    article_title = request.POST.get('title')
    article_content = request.POST.get('content')

    article_dict = {
        'title': article_title,
        'content': article_content,
        'category': article_category,
        'tag_list': tag_list
    }

    new_article = createArticle(**article_dict)

    return HttpResponse('%s 번째 글 저장이 정상 처리 되었습니다' % new_article.id)


def checkWriteForm(request):
    if request.POST.has_key('title') is False:
        return False
    elif request.POST.has_key('content') is False:
        return False

    if len(request.POST.get('title')) is 0:
        return False

    if len(request.POST.get('content')) is 0:
        return False

    return True


def updateTag(tags):
    tag_list = []
    if len(tags) is 0:
        return tag_list

    tag_list = map(lambda tag: Tag.objects.get_or_create(name=tag)[0], tags)
    return tag_list

@transaction.commit_manually
def createArticle(**kwargs):
    new_article = Article(title=kwargs['title'], content=kwargs.get('content'), category=kwargs.get('category'))

    try:
        new_article.save()

        if len(kwargs.get('tag_list')) > 0:
            for tag in kwargs.get('tag_list'):
                new_article.tags.add(tag)
    except:
        return HttpResponse('블로그 글 저장중 오류가 발생 하였습니다')

    transaction.commit()

    return new_article