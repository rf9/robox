from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import FormView
from .forms import UploadFileForm
from .recording import record
from .parsing import parse
from .models import File


def index(request):
    return render(request, 'garage/index.html')


class UploadView(FormView):
    template_name = "garage/upload.html"
    form_class = UploadFileForm

    def form_valid(self, form):
        filedata = self.get_form_kwargs().get('files')['file']
        barcode = form.cleaned_data['barcode']
        f = handle_uploaded_file(barcode, filedata)
        return HttpResponseRedirect(reverse('garage:file_detail', args=(f.pk,)))


# def upload(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(form.sample, request.FILES['file'])
#             return HttpResponseRedirect(reverse('garage:uploaded'))
#     else:
#         form = UploadFileForm()
#     return render(request, 'garage/upload.html', {'form': form})


def handle_uploaded_file(barcode, f):
    rowdata = parse(f)
    return record(barcode, f.name, rowdata)


def uploaded(request):
    return render(request, 'garage/uploaded.html')


def add_bool(s, x):
    l = len(s)
    s.add(x)
    return len(s) > l


def file_detail(request, file_id):
    f = get_object_or_404(File, pk=int(file_id))
    headings = f.headings()
    tabledata = f.table_content(headings)

    context = {'file': f, 'headings': headings, 'tabledata': tabledata}
    return render(request, 'garage/file_detail.html', context)
