from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # /garage/
    url(r'^upload/$', views.UploadView.as_view(), name='upload'), # /garage/upload/
    url(r'^uploaded/$', views.uploaded, name='uploaded'), # /garage/uploaded/
    url(r'^file/(?P<file_id>[0-9]+)/$', views.file_detail, name='file_detail'), # /garage/file/7/
]