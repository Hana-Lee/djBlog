# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import Context, loader, RequestContext

import hashlib

from dBlog.models import Article, Category, Comment
from dBlog import service


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

    data_dict = ({
        'page_title': page_title,
        'articles': articles,
        'current_page': page_no
    })
    return render_to_response('list.html', data_dict, context_instance=RequestContext(request))


def read(request, article_id=None):
    page_title = '블로그 글 읽기'

    try:
        current_article = Article.objects.get(id=int(article_id))
    except:
        return HttpResponse('%d 에 해당하는 글이 존재 하지 않습니다' % article_id)
    try:
        prev_article = current_article.get_previous_by_created()
    except:
        prev_article = None

    try:
        next_article = current_article.get_next_by_created()
    except:
        next_article = None

    comments = Comment.objects.filter(article=current_article).order_by('created')

    data_dict = ({
        'page_title': page_title,
        'current_article': current_article,
        'prev_article': prev_article,
        'next_article': next_article,
        'comments' : comments
    })

    return render_to_response('read.html', data_dict, context_instance=RequestContext(request))


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
        tag_list = service.updateTag(tags)

    article_title = request.POST.get('title')
    article_content = request.POST.get('content')

    article_dict = {
        'title': article_title,
        'content': article_content,
        'category': article_category,
        'tag_list': tag_list
    }

    new_article = service.createArticle(**article_dict)

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


def add_comment(request):
    cmt_name = request.POST.get('name', '')
    if not cmt_name.strip():
        return HttpResponse('이름 입력은 필수 입니다.')

    cmt_pwd = request.POST.get('password', '')
    if not cmt_pwd.strip():
        return HttpResponse('비밀번호를 입력해주세요')

    cmt_pwd = hashlib.md5(cmt_pwd).hexdigest()

    cmt_content = request.POST.get('content', '')
    if not cmt_content.strip():
        return HttpResponse('내용을 입력해주세요')

    cmt_email = request.POST.get('email', '')

    article_id = request.POST.get('article_id', '')
    current_article = Article.objects.get(id=article_id)

    cmt_dict = dict(name=cmt_name, password=cmt_pwd, content=cmt_content, email=cmt_email, article=current_article)

    service.update_comment(**cmt_dict)

    return redirect('/blog/article/%s/' % article_id)


def del_comment(request):
    cmt_id = request.POST.get('cmt_id', '')
    if not cmt_id.strip():
        return HttpResponse('댓글 아이디가 존재 하지 않습니다.')

    cmt_pwd = request.POST.get('password', '')
    if not cmt_pwd.strip():
        return HttpResponse('비밀번호 입력이 잘못 되었습니다.')

    article_id = request.POST.get('article_id', '')

    cmt_pwd = hashlib.md5(cmt_pwd).hexdigest()

    service.delete_comment(cmt_id, cmt_pwd)

    return redirect('/blog/article/%s/' % article_id)

def del_article(request):
    article_id = request.POST.get('article_id', '')
    if not article_id:
        return HttpResponse('블로그 글 아이디가 존재하지 않습니다.')

    service.delete_article(article_id)

    return redirect('/blog/')

def view_category(request):
    page_title = '카테고리 관리'
    categories = Category.objects.all()

    data_dict = ({
                     'page_title': page_title,
                     'categories': categories
                 })
    return render_to_response('write_category.html', data_dict, context_instance=RequestContext(request))

def add_category(request):
    category_name = request.POST.get('category_name', '')
    print len(category_name)
    if len(category_name) is 0:
        return HttpResponse('카테고리 이름이 없습니다.')

    service.create_category(category_name)

    return redirect('/blog/')

def del_category(request):
    category_id = request.POST.get('category_id', '')
    if not category_id:
        return HttpResponse('카테고리 아이디가 없습니다.')

    service.delete_category(category_id)

    return redirect('/blog/add/category')