"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os
from django.test import TestCase, Client
from django.conf import settings

from dBlog.models import Article, Category
from dBlog.service import BlogService


class BlogModelsTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='first')
        Article.objects.create(
            title = 'first blog',
            content = 'content',
            category = category
        )

    def test_category(self):
        first_category = Category.objects.get(id=1)
        self.assertEqual(first_category.name, 'first')

    def test_article(self):
        first_article = Article.objects.get(id=1)
        self.assertEqual(first_article.title, 'first blog')


class BlogRequestResponseTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='first')
        Article.objects.create(
            title = 'first blog',
            content = 'content',
            category = category
        )

        test_template_dirs = os.path.dirname(__file__)
        settings.TEMPLATE_DIRS = (test_template_dirs + '/template/',)

    def test_article_response(self):
        c = Client()
        response = c.get('/blog/article/1/')
        self.assertEqual(response.status_code, 200)

    def test_blog_list_response(self):
        c = Client()
        response = c.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_page_response(self):
        c = Client()
        response = c.get('/blog/page/1/')
        self.assertEqual(response.status_code, 200)

				
class BlogViewTest(TestCase):
	def setUp(self):
		category = Category.objects.create(name='first')
