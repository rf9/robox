from django.conf.urls import url
from django.views.generic import RedirectView
from rest_framework import routers

from robox.views import web, api, docs

router = routers.SimpleRouter()
router.register(r'api/files', api.FileViewSet, base_name='file')

urlpatterns = [
    # URLs for the webapp.
    url(r'^upload/$', web.UploadView.as_view(), name="upload"),
    url(r'^view/(?P<barcode>\S+)/$', web.view_by_barcode, name="view"),
    url(r'^upload/(?P<barcode>\S+)/$', web.upload_by_barcode, name="upload_barcode"),
    url(r'^view/$', web.index, name="index"),
    url(r'^delete/(?P<pk>[0-9]+)/$', web.FileDelete.as_view(), name='delete_file'),
    url(r'^search/$', web.search, name="search"),
                  url(r'^$', RedirectView.as_view(url='/view/', permanent=True), name='root'),

    # URLS for the documentation
    url(r'^docs/$', docs.index, name="docs_index"),
    url(r'^docs/api/$', docs.api, name="docs_api"),
    url(r'^docs/parsers/$', docs.parsers, name="docs_parsers"),
              ] + router.urls
