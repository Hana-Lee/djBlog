from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djBlog.views.home', name='home'),
    # url(r'^djBlog/', include('djBlog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^blog/$', 'dBlog.views.index'),
    url(r'^blog/page/(?P<page>\d+)/$', 'dBlog.views.index'),
    url(r'^blog/article/(?P<article_id>\d+)/$', 'dBlog.views.read'),
    url(r'^blog/write/$', 'dBlog.views.write_form'),
    url(r'^blog/add/post/$', 'dBlog.views.add_post')

)
