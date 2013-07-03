# -*- coding: utf-8 -*-
from django.db import transaction, DatabaseError

from dBlog.models import Comment, Article, Tag, Category


class BlogService(object):
    def __init__(self):
        pass

    @transaction.commit_on_success
    def save(self, *model, **models):
        if 'save' in dir(model):
            try:
                model[0].save()
            except DatabaseError, e:
                error_msg = model.__class__.__name__ + ' 을 세이브 도중 오류가 발생 하였습니다 : %s'
                raise DatabaseError(error_msg % e)

    @transaction.commit_on_success
    def delete(self, *model, **models):
        if 'delete' in dir(model):
            try:
                model[0].delete()
            except DatabaseError, e:
                error_msg = model.__class__.__name__ + ' 을 삭제 도중 오류가 발생 하였습니다. : %s'
                raise DatabaseError(error_msg % e)

    def get(self, model_id=None, *model):
        if model_id is None:
            raise Exception('id 는 필수로 넘겨 주어야 합니다.')

        if model is None:
            raise Exception('Model 은 필수로 넘겨 주어야 하비다.')

        if 'objects' in dir(model[0]):
            try:
                mdl = Article(model[0])
                print dir(mdl)
                return mdl.objects.get(id=int(model_id))
            except DatabaseError, e:
                error_msg = model.__class__.__name__ + ' 을 가져오는 도중 오류가 발생 하였습니다. %s'
                raise DatabaseError(error_msg % e)


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

        update_article_comment_count(kwargs.get('article').id)
    except DatabaseError, e:
        error_msg = '댓글 저장중 오류가 발생 하였습니다. %s'
        raise DatabaseError(error_msg % e)

    transaction.commit()

    return new_cmt


@transaction.commit_on_success
def update_article_comment_count(article_id):
    try:
        target_article = Article.objects.get(id=article_id)
        if not target_article:
            raise DatabaseError('아이디 %d 에 해당하는 블로그 글을 가져오는데 실패 했습니다.' % article_id)

        target_article.comments += 1
        target_article.save()
    except Exception, e:
        error_msg = '블로그 글의 댓글 갯수를 업데이트 도중 오류가 발생하였습니다. %s'
        raise DatabaseError(error_msg % e)


@transaction.commit_on_success
def delete_comment(comment_id, password):
    try:
        target = Comment.objects.get(id=comment_id, password=password)
        if target is None:
            raise ValueError('댓글을 가져오는데 실패 하였습니다. 비밀번호를 확인하세요.')

        target.delete()
    except DatabaseError, e:
        raise DatabaseError(e)


@transaction.commit_on_success
def delete_article(article_id):
    try:
        target = Article.objects.get(id=article_id)
        if target is None:
            raise ValueError('삭제하려는 블로그가 존재 하지 않습니다.')

        target.delete()
    except DatabaseError, e:
        raise DatabaseError(e)


@transaction.commit_on_success
def delete_category(category_id):
    try:
        target = Category.objects.get(id=category_id)
        if target is None:
            raise ValueError('카테고리 삭제에 실패 하였습니다.')

        target.delete()
    except DatabaseError, e:
        raise DatabaseError(e)

def create_category(category_name):
    try:
        category = Category(name=category_name)
        category.save()
    except DatabaseError, e:
        raise DatabaseError('카테고리 저장에 실패 하였습니다.')