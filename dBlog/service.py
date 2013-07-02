# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.db import transaction, DatabaseError

from dBlog.models import Comment, Article, Tag


def updateTag(tags):
    tag_list = []
    if len(tags) is 0:
        return tag_list

    try:
        tag_list = map(lambda tag: Tag.objects.get_or_create(name=tag)[0], tags)
    except Exception, e:
        error_msg = '태그 업그레이드 도중 오류가 났습니다. %s'
        raise DatabaseError(error_msg % e)

    return tag_list


@transaction.commit_manually
def createArticle(**kwargs):
    new_article = Article(title=kwargs['title'], content=kwargs.get('content'), category=kwargs.get('category'))

    try:
        new_article.save()

        if len(kwargs.get('tag_list')) > 0:
            for tag in kwargs.get('tag_list'):
                new_article.tags.add(tag)
    except Exception, e:
        error_msg = '블로그 글 저장 중 오류가 발생 하였습니다. %s'
        raise DatabaseError(error_msg % e)

    transaction.commit()

    return new_article

@transaction.commit_manually
def update_comment(**kwargs):
    new_cmt = Comment(
        name=kwargs.get('name'),
        password=kwargs.get('password'),
        email=kwargs.get('email'),
        content=kwargs.get('content'),
        article=kwargs.get('article')
    )
    try:
        new_cmt.save()

        article = Article.objects.get(id=kwargs.get('article').id)
        article.comments += 1
        article.save()
    except DatabaseError, e:
        error_msg = '댓글 저장중 오류가 발생 하였습니다. %s'
        raise DatabaseError(error_msg % e)
    transaction.commit()
    return new_cmt