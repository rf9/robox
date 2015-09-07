from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, DeleteView

from parsers import parsing
from robox.forms import UploadForm
from robox.models import File, Entry, MetaData
from parsers.parsing import RoboxParsingError


def index(request):
    files = File.objects.all()

    return render(request, "robox/index.html", {"files": files})


class UploadView(FormView):
    template_name = "robox/upload.html"
    form_class = UploadForm

    def form_valid(self, form):
        file = self.request.FILES['file']

        try:
            parsed_file = parsing.parse(file)
            database_file = File.objects.create(
                file=file,
                barcode=form.cleaned_data['barcode'],
                format=parsed_file['parser'],
            )

            for data in parsed_file['data']:
                entry = Entry.objects.create(file=database_file)
                for key, value in data.items():
                    MetaData.objects.create(entry=entry, key=key, value=value)
        except RoboxParsingError:
            database_file = File.objects.create(
                file=file,
                barcode=form.cleaned_data['barcode'],
            )

        return HttpResponseRedirect(reverse('view', kwargs={'barcode': database_file.barcode}))


def view_by_barcode(request, barcode):
    files = File.objects.filter(barcode=barcode)

    return render(request, "robox/view.html", {'files': files, 'barcode': barcode})


class FileDelete(DeleteView):
    model = File
    success_url = reverse_lazy('index')
