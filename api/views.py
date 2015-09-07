from django.http import HttpResponse
from django_extensions.db.fields import json
from robox.models import File, Entry, MetaData


def get_by_barcode(request, barcode):
    response_data = {
        'barcode': barcode,
        'files': [],
    }

    for file in File.objects.filter(barcode=barcode):
        file_json = {
            'upload_time': file.upload_time,
            'file_type': file.format,
            'file': request.build_absolute_uri(file.file.url),
            'data': [],
        }

        for entry in file.entry_set.all():
            data_json = {}
            for meta_data in entry.metadata_set.all():
                data_json[meta_data.key] = meta_data.value

            file_json['data'].append(data_json)

        response_data['files'].append(file_json)

    return HttpResponse(json.dumps(response_data), content_type='application/json')
