from django.conf.urls import url, patterns
from docs import views

__author__ = 'rf9'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^api/$', views.api, name="api"),
    url(r'^parsers/$', views.parsers, name="parsers"),
]

