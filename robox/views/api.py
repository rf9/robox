from http import client
import logging

from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from django_extensions.db.fields import json

from robox.models import DataFile
from robox.utils import upload_files, validate_barcode

_logger = logging.getLogger(__name__)


def get_by_barcode(request, barcode):
    try:
        validate_barcode(barcode)

        response_data = {
            'barcode': barcode,
            'files': [serialise_file(file) for file in DataFile.objects.filter(barcode=barcode)],
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')
    except ValidationError:
        return HttpResponse(json.dumps({'error': 'Invalid barcode', 'barcode': barcode}),
                            content_type='application/json',
                            status=client.UNPROCESSABLE_ENTITY)


@csrf_exempt
@atomic
def upload(request):
    files = request.FILES
    barcode = request.REQUEST.get('barcode')

    try:
        validate_barcode(barcode)

        database_files = upload_files(barcode, [file for file in files.values()])
        response_data = {
            'barcode': barcode,
            'files': [serialise_file(file) for file in database_files],
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=client.CREATED)
    except ValidationError:
        return HttpResponse(json.dumps({'error': 'Invalid barcode', 'barcode': barcode}),
                            content_type='application/json',
                            status=client.UNPROCESSABLE_ENTITY)


def serialise_file(file):
    file_json = {
        'upload_time': file.upload_time,
        'file_type': file.format,
        'file': file.binary_file.name,
        'data': [],
    }

    for entry in file.entry_set.all():
        data_json = {}
        for meta_datum in entry.metadata_set.all():
            data_json[meta_datum.key] = meta_datum.value

        file_json['data'].append(data_json)

    return file_json
