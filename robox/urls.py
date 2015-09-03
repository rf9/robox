from django.conf.urls import url

from robox import views

urlpatterns = [
    url(r'^upload/$', views.UploadView.as_view(), name="upload"),
    url(r'^view/(?P<barcode>\S+)/$', views.view, name="view"),
    url(r'^view/$', views.index, name="index"),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.FileDelete.as_view(), name='delete_file'),
]
