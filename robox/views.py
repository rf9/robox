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

        file = self.get_form_kwargs().get('files')['file']
        datas = []
        parser_name = "None"
        parsers = get_parsers()
        for (parser, name) in parsers:
            file_data = parser.parse(file)
            if file_data is not None:
                datas.append(file_data)
                parser_name = name

        database_file = File.objects.create(
            file=file,
            barcode=form.cleaned_data['barcode'],
            format=parser_name,
        )

        if len(datas) == 1:
            for data in datas[0].data:
                entry = Entry.objects.create(file=database_file)
                for key in data.meta:
                    MetaData.objects.create(entry=entry, key=key, value=data.meta[key])

        return HttpResponseRedirect(reverse('view', kwargs={'barcode': database_file.barcode}))


def view(request, barcode):
    files = File.objects.filter(barcode=barcode)

    return render(request, "robox/view.html", {"files": files})


class FileDelete(DeleteView):
    model = File
    success_url = reverse_lazy('index')
