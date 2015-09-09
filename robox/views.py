from django.core.urlresolvers import reverse, reverse_lazy
from django.db import DatabaseError
from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, DeleteView

from robox.forms import UploadForm
from robox.models import File


def index(request):
    files = File.objects.all()

    return render(request, "robox/index.html", {"files": files})


def search(request):
    barcode = request.GET.get('barcode')
    if barcode:
        return HttpResponseRedirect(reverse('view', kwargs={'barcode': barcode}))
    else:
        return HttpResponseRedirect(reverse('index'))


class UploadView(FormView):
    template_name = "robox/upload.html"
    form_class = UploadForm

    def form_valid(self, form):
        file = self.request.FILES['file']
        barcode = form.cleaned_data['barcode']

        database_file = upload_file(barcode, file)

        return HttpResponseRedirect(reverse('view', kwargs={'barcode': database_file.barcode}))


@atomic
def upload_file(barcode, file):
    barcode = barcode.upper()
    try:
        database_file = File.objects.create(
            file=file,
            barcode=barcode,
        )
        database_file.parse()
    except DatabaseError as err:
        try:
            # noinspection PyUnboundLocalVariable
            database_file.file.delete()
        except NameError:
            pass
        raise err

    return database_file


def view_by_barcode(request, barcode):
    files = File.objects.filter(barcode=barcode)

    return render(request, "robox/view.html", {'files': files, 'barcode': barcode})


class FileDelete(DeleteView):
    model = File
    success_url = reverse_lazy('index')
