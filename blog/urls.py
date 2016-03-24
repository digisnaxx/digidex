from django.conf.urls import patterns, url
from django.views.generic import DetailView

from models import Post, Category, Tag
from .views import *

urlpatterns = patterns('',  # Index
                       url(r'^$', index, name='index'),
                       url(r'^(?P<selected_page>\d+)/?$', 'blog.views.index'),

                       # Individual Posts
                       url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$',
                           DetailView.as_view(
                               model=Post,
                           )),

                       url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryListView.as_view(
                           paginate_by=8,
                           model=Category,
                       )),

                       url(r'^tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagListView.as_view(
                           paginate_by=8,
                           model=Tag,
                       )),

                       url(r'^about', about, name='about'),
                       # url(r'^cancel', cancel, name='cancel'),
                       )
