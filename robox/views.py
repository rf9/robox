from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, DeleteView

from robox.forms import UploadForm
from robox.models import File, Entry, MetaData
from robox.parsers import get_parsers


def index(request):
    files = File.objects.all()

    return render(request, "robox/index.html", {"files": files})


class UploadView(FormView):
    template_name = "robox/upload.html"
    form_class = UploadForm

    def form_valid(self, form):
        file = self.request.FILES['file']
        successful_parses = []
        parsers = get_parsers()
        for (parser, name) in parsers:
            file_data = parser.parse(file)
            if file_data is not None:
                successful_parses.append({"parsed_data": file_data, "parser": name})

        if len(successful_parses) == 1:
            successful_parse = successful_parses[0]
            database_file = File.objects.create(
                file=file,
                barcode=form.cleaned_data['barcode'],
                format=successful_parse['parser'],
            )

            for data in successful_parse['parsed_data'].data:
                entry = Entry.objects.create(file=database_file)
                for key in data.meta:
                    MetaData.objects.create(entry=entry, key=key, value=data.meta[key])
        else:
            database_file = File.objects.create(
                file=file,
                barcode=form.cleaned_data['barcode'],
            )

        return HttpResponseRedirect(reverse('view', kwargs={'barcode': database_file.barcode}))


def view_by_barcode(request, barcode):
    files = File.objects.filter(barcode=barcode)

    return render(request, "robox/view.html", {"files": files, "barcode": barcode})


class FileDelete(DeleteView):
    model = File
    success_url = reverse_lazy('index')
