import logging
import json

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import DatabaseError
from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, DeleteView
import pika
from pika.exceptions import ConnectionClosed

from robox.forms import UploadForm, validate_barcode
from robox.models import File

_logger = logging.getLogger(__name__)


def index(request):
    files = File.objects.all().order_by('-upload_time')[:20]

    return render(request, "robox/robox/index.html", {"files": files})


def search(request):
    barcode = request.GET.get('barcode')
    if barcode:
        return HttpResponseRedirect(reverse('view', kwargs={'barcode': barcode}))
    else:
        return HttpResponseRedirect(reverse('index'))


class UploadView(FormView):
    template_name = "robox/robox/upload.html"
    form_class = UploadForm

    def form_valid(self, form):
        files = self.request.FILES
        barcode = form.cleaned_data['barcode']

        database_files = upload_files(barcode, [file for file_key in files.keys() for file in files.getlist(file_key)])

        return HttpResponseRedirect(reverse('view', kwargs={'barcode': database_files[0].barcode}))


@atomic
def upload_files(barcode, files):
    """
    Atomically uploads a file to the database and parses it.
    :param barcode: The barcode for the file to be uploaded to.
    :param files: The Django files to be uploaded
    :return: The database model of the uploaded file.
    """
    barcode = barcode
    database_files = []

    for file in files:
        try:
            database_file = File.objects.create(
                file=file,
                barcode=barcode,
            )
            database_file.parse()
            database_files.append(database_file)
        except DatabaseError as err:
            try:
                # noinspection PyUnboundLocalVariable
                database_file.file.delete()
            except NameError:
                pass
            raise err

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue="upload_notifier")

        channel.basic_publish(exchange='',
                              routing_key='upload_notifier',
                              body=json.dumps({"barcode": barcode, "file_count": len(database_files)}))

        connection.close()
        _logger.debug("Sent message to message queue.")
    except ConnectionClosed:
        _logger.warning("rabbitmq server not responding.")

    return database_files


def view_by_barcode(request, barcode):
    barcode = barcode
    try:
        validate_barcode(barcode)
        files = File.objects.filter(barcode=barcode)

        return render(request, "robox/robox/view.html", {'files': files, 'barcode': barcode})
    except ValidationError:
        return render(request, "robox/robox/view.html", {'invalid': True, 'barcode': barcode})


def upload_by_barcode(request, barcode):
    files = request.FILES

    database_files = upload_files(barcode, [file for file_key in files.keys() for file in files.getlist(file_key)])

    return HttpResponseRedirect(reverse('view', kwargs={'barcode': database_files[0].barcode}))


class FileDelete(DeleteView):
    model = File
    success_url = reverse_lazy('index')
