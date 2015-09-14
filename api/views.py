from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_extensions.db.fields import json

from robox.forms import validate_barcode
from robox.models import File
from robox.views import upload_files


def get_by_barcode(request, barcode):
    try:
        validate_barcode(barcode)

        barcode = barcode
        response_data = {
            'barcode': barcode,
            'files': [serialise_file(file, request) for file in File.objects.filter(barcode=barcode)],
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')
    except ValidationError:
        return HttpResponse(json.dumps({'error': 'Invalid barcode', 'barcode': barcode}),
                            content_type='application/json',
                            status=422)


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
            'files': [serialise_file(file, request) for file in database_files],
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')
    except ValidationError:
        return HttpResponse(json.dumps({'error': 'Invalid barcode', 'barcode': barcode}),
                            content_type='application/json',
                            status=422)


def serialise_file(file, request=None):
    file_json = {
        'upload_time': file.upload_time,
        'file_type': file.format,
        'file': request.build_absolute_uri(file.file.url) if request else file.file.url,
        'data': [],
    }

    for entry in file.entry_set.all():
        data_json = {}
        for meta_datum in entry.metadata_set.all():
            data_json[meta_datum.key] = meta_datum.value

        file_json['data'].append(data_json)

    return file_json
