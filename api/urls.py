from django.conf.urls import url, patterns
from api import views

__author__ = 'rf9'

urlpatterns = [
    url(r'^barcode/(?P<barcode>\S+)/$', views.get_by_barcode, name="barcode"),
    url(r'^upload/$', views.upload, name='upload')
]
