from django.contrib import admin
from dBlog.model import *

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)