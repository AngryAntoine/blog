from django.conf.urls import url
from .views import (
    PostCreateAPIView,
    PostDeleteAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostUpdateAPIView,
)

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list'),
    url(r'^create/$', PostCreateAPIView.as_view(), name='blog_post_create'),
    url(r'^(?P<slug>[a-z0-9-]+)/$', PostDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<slug>[a-z0-9-]+)/edit/$', PostUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<slug>[a-z0-9-]+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),
]
