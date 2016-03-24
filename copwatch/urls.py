from django.conf.urls import patterns, url
from django.views.generic.detail import DetailView

from . import views
from .models import Officer

urlpatterns = [
				url(r'^$', views.main, name='main'),
				# url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
				# 	OfficerDetail.as_view(template_name="officer_detail.html"), name='officer-detail'),
				# url(r'^(?P<pk>\d+)/(?P<slug>[a-zA-Z0-9-]+)/?$',
				# 	DetailView.as_view(
				# 		model=Officer,
				# 		template_name="officer_detail.html",
				# 	)),
				url(r'^(?P<pk>[0-9]+)/(?P<rank>[a-zA-Z0-9-]+)/(?P<slug>[a-zA-Z0-9-]+)/$',
				views.DetailView.as_view(),
				name='officer_detail'),
            ]
