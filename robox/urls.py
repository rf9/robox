from django.conf.urls import url, patterns
from django.views.generic import RedirectView

from robox import views

urlpatterns = [
    url(r'^upload/$', views.UploadView.as_view(), name="upload"),
    url(r'^view/(?P<barcode>\S+)/$', views.view_by_barcode, name="view"),
    url(r'^upload/(?P<barcode>\S+)/$', views.upload_by_barcode, name="upload_barcode"),
    url(r'^view/$', views.index, name="index"),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.FileDelete.as_view(), name='delete_file'),
    url(r'^search/$', views.search, name="search"),
    url(r'^$', RedirectView.as_view(url='/view/', permanent=True)),
]
