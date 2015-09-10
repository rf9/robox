from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import DatabaseError
from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, DeleteView

from robox.forms import UploadForm, validate_barcode
from robox.models import File


def index(request):
    files = File.objects.all().order_by('-upload_time')[:20]

    return render(request, "robox/index.html", {"files": files})


def search(request):
    barcode = request.GET.get('barcode')
    if barcode:
        return HttpResponseRedirect(reverse('robox:view', kwargs={'barcode': barcode}))
    else:
        return HttpResponseRedirect(reverse('robox:index'))


class UploadView(FormView):
    template_name = "robox/upload.html"
    form_class = UploadForm

    def form_valid(self, form):
        files = self.request.FILES
        barcode = form.cleaned_data['barcode']

        database_files = [upload_file(barcode, files.get(file_name)) for file_name in files.keys()]

        return HttpResponseRedirect(reverse('robox:view', kwargs={'barcode': database_files[0].barcode}))


@atomic
def upload_file(barcode, file):
    """
    Atomically uploads a file to the database and parses it.
    :param barcode: The barcode for the file to be uploaded to.
    :param file: The Django file to be uploaded
    :return: The database model of the uploaded file.
    """
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
    barcode = barcode.upper()
    try:
        validate_barcode(barcode)
        files = File.objects.filter(barcode=barcode)

        return render(request, "robox/view.html", {'files': files, 'barcode': barcode})
    except ValidationError:
        return render(request, "robox/view.html", {'invalid': True, 'barcode': barcode})


def upload_by_barcode(request, barcode):
    files = request.FILES

    database_files = [upload_file(barcode, files.get(file_name)) for file_name in files.keys()]

    return HttpResponseRedirect(reverse('robox:view', kwargs={'barcode': database_files[0].barcode}))


class FileDelete(DeleteView):
    model = File
    success_url = reverse_lazy('robox:index')
