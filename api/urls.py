from django.conf.urls import url
from api import views

__author__ = 'rf9'

urlpatterns = [
    url(r'^barcode/(?P<barcode>\S+)/$', views.barcode, name="barcode"),
]