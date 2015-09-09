import json

from django.shortcuts import render


def index(request):
    return render(request, "docs/index.html")


def api(request):
    code_blocks = {
        "barcode_response_success_format": {"barcode": "barcode", "files": [{"upload_time": "datetime", "data": [{"key": "value", }], "file": "urlpath", "file_type": "string"}]},
        "barcode_response_success_example": {"barcode": "ABC001", "files": [{"upload_time": "2015-09-09T12:14:05.350Z","data": [{"value": "48.8164672349381","units": "nM", "address": "A1","name": "concentration"},{"value": "33.33333333333333","units": "%", "address": "A1","name": "dilution"},{"value": "54.134358195761","units": "nM", "address": "B1","name": "concentration"},{"value": "33.33333333333333","units": "%", "address": "B1","name": "dilution"}, ],"file": "/media/data/Caliper1_411709_PATH_1_3_2015-08-18_01-24-55_WellTable_neqrdbc.csv","file_type": "wgs"}]},
        "barcode_response_success_empty_example": {"barcode": "ABC002", "files": []},
        "upload_response_success_format": {"barcode": "barcode", "files": [{"upload_time": "datetime", "data": [{"key": "value", }], "file": "urlpath", "file_type": "string"}]},
        "upload_response_success_example": {"barcode": "ABC001", "files": [{"upload_time": "2015-09-09T12:14:05.350Z","data": [{"value": "48.8164672349381","units": "nM", "address": "A1","name": "concentration"},{"value": "33.33333333333333","units": "%", "address": "A1","name": "dilution"},{"value": "54.134358195761","units": "nM", "address": "B1","name": "concentration"},{"value": "33.33333333333333","units": "%", "address": "B1","name": "dilution"}, ],"file": "/media/data/Caliper1_411709_PATH_1_3_2015-08-18_01-24-55_WellTable_neqrdbc.csv","file_type": "wgs"}]},
        "upload_response_error_format": {"barcode": "barcode", "error": "message"},
        "upload_response_error_example": {"barcode": "123456789", "error": "Invalid barcode"},
    }
    code_blocks = {name: json.dumps(block, indent=4) for name, block in code_blocks.items()}

    return render(request, "docs/api.html", code_blocks)


def parsers(request):
    return render(request, "docs/parsers.html")
