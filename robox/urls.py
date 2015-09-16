from django.conf.urls import url
from django.views.generic import RedirectView

from robox.views import robox, api, docs

urlpatterns = [
    url(r'^upload/$', robox.UploadView.as_view(), name="upload"),
    url(r'^view/(?P<barcode>\S+)/$', robox.view_by_barcode, name="view"),
    url(r'^upload/(?P<barcode>\S+)/$', robox.upload_by_barcode, name="upload_barcode"),
    url(r'^view/$', robox.index, name="index"),
    url(r'^delete/(?P<pk>[0-9]+)/$', robox.FileDelete.as_view(), name='delete_file'),
    url(r'^search/$', robox.search, name="search"),
    url(r'^$', RedirectView.as_view(url='/view/', permanent=True)),

    url(r'^api/barcode/(?P<barcode>\S+)/$', api.get_by_barcode, name="api_barcode"),
    url(r'^api/upload/$', api.upload, name='api_upload'),

    url(r'^docs/$', docs.index, name="docs_index"),
    url(r'^docs/api/$', docs.api, name="docs_api"),
    url(r'^docs/parsers/$', docs.parsers, name="docs_parsers"),
]
