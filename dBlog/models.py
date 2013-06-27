from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40, null=False)


class Tag(models.Model):
    name = models.CharField(max_length=30, null=False)


class Article(models.Model):
    title = models.CharField(max_length=80, null=False)
    content = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag)
    comments = models.PositiveSmallIntegerField(default=0, null=True)

    class Admin:
        pass


class Comment(models.Model):
    content = models.TextField(null=False)
    email = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=30, null=False)
    modEnabled = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(auto_now=True)
    article = models.ForeignKey(Article)