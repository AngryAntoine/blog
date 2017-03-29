from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', blog_home, name='blog_home'),
    url(r'^create/$', blog_post_create, name='blog_post_create'),
    url(r'^(?P<slug>[a-z0-9-]+)/$', blog_post_detail, name='blog_post_detail'),
    url(r'^(?P<slug>[a-z0-9-]+)/edit/$', blog_post_update, name='blog_post_update'),
    url(r'^(?P<slug>[a-z0-9-]+)/delete/$', blog_post_delete, name='blog_post_delete'),
]
