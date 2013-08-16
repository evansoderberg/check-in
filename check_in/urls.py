from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from check_in import views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^entry/$', views.CheckinList.as_view()),
    url(r'^entry/(?P<pk>[0-9]+)/$', views.CheckinDetail.as_view()),
    url(r'^$', 'check_in.views.index', name='index'),
    url(r'^add/$', 'check_in.views.add_entry'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
