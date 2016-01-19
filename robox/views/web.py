import logging

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.encoding import smart_str
from django.views.generic import FormView, DeleteView

from robox.forms import UploadForm
from robox.models import DataFile, BinaryFile
from robox.utils import upload_files, validate_barcode

_logger = logging.getLogger(__name__)


def index(request):
    files = DataFile.objects.all().order_by('-upload_time')[:15]

    return render(request, "robox/web/index.html", {"files": files})


def search(request):
    barcode = request.GET.get('barcode')
    if barcode:
        return HttpResponseRedirect(reverse('view', kwargs={'barcode': barcode}))
    else:
        return HttpResponseRedirect(reverse('index'))


class UploadView(FormView):
    template_name = "robox/web/upload.html"
    form_class = UploadForm

    def form_valid(self, form):
        files = self.request.FILES
        barcode = form.cleaned_data['barcode']

        database_files = upload_files(barcode, [file for file_key in files.keys() for file in files.getlist(file_key)])

        return HttpResponseRedirect(reverse('view', kwargs={'barcode': database_files[0].barcode}))


def view_by_barcode(request, barcode):
    barcode = barcode
    try:
        validate_barcode(barcode)
        files = DataFile.objects.filter(barcode__iexact=barcode)

        return render(request, "robox/web/view.html", {'files': files, 'barcode': barcode})
    except ValidationError:
        return render(request, "robox/web/view.html", {'invalid': True, 'barcode': barcode})


def upload_by_barcode(request, barcode):
    files = request.FILES

    database_files = upload_files(barcode, [file for file_key in files.keys() for file in files.getlist(file_key)])

    return HttpResponseRedirect(reverse('view', kwargs={'barcode': database_files[0].barcode}))


class FileDelete(DeleteView):
    model = DataFile
    success_url = reverse_lazy('index')


def download_file(request, pk):
    file = get_object_or_404(BinaryFile, pk=pk)

    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file.name)
    response.write(file.data)

    return response
