from ast import literal_eval
import json
import os

from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase
from mock import MagicMock
import mock

from api.views import get_by_barcode, upload
from mainsite import settings

from robox.models import File


class APIGetTests(TestCase):
    barcode = "0000000000000"

    def setUp(self):
        with open(os.path.join(settings.BASE_DIR,
                               "parsing/testFiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv"),
                  'rb') as f:
            self.file = File.objects.create(barcode=self.barcode, file=UploadedFile(file=f))
        self.file.parse()
        self.file.refresh_from_db()

    def test_with_valid_barcode(self):
        api_results = get_by_barcode(None, self.barcode)
        self.assertEqual(200, api_results.status_code)
        content = json.loads(api_results.content.decode("ascii"))

        self.assertEqual(self.barcode, content["barcode"])
        self.assertEqual(list, type(content['files']))
        self.assertEqual(1, len(content['files']))
        file = content['files'][0]
        self.assertTrue('data' in file)
        self.assertTrue('upload_time' in file)
        self.assertTrue('file' in file)
        self.assertTrue('file_type' in file)

    def test_with_invalid_barcode(self):
        api_results = get_by_barcode(None, "fake_barcode")
        self.assertEqual(422, api_results.status_code)
        content = json.loads(api_results.content.decode("ascii"))

        self.assertEqual("fake_barcode", content['barcode'])
        self.assertEqual('Invalid barcode', content['error'])

    def tearDown(self):
        self.file.delete()


def mock_return(value):
    for file in value['files']:
        file['file'] = 'mock_file_path'
        file['upload_time'] = "upload_time"

    return str(value)


class APIPostTestsValidBarcode(TestCase):
    barcode = "0000000000000"

    @mock.patch('django_extensions.db.fields.json.dumps', side_effect=mock_return)
    def setUp(self, *save_mock):
        self.file_count = File.objects.filter(barcode=self.barcode).count()

        with open(os.path.join(settings.BASE_DIR,
                               "parsing/testFiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv"),
                  'rb') as f:
            self.api_results = upload(MagicMock(FILES={"any": UploadedFile(file=f)}, REQUEST={"barcode": self.barcode}))

    def test_correct_response_data(self):
        self.assertEqual(200, self.api_results.status_code)
        content = literal_eval(self.api_results.content.decode("ascii"))

        self.assertEqual(self.barcode, content["barcode"])
        self.assertEqual(list, type(content['files']))
        self.assertEqual(1, len(content['files']))
        file = content['files'][0]
        self.assertTrue('data' in file)
        self.assertTrue('upload_time' in file)
        self.assertTrue('file' in file)
        self.assertTrue('file_type' in file)

    def test_file_added_to_database(self):
        files = File.objects.filter(barcode=self.barcode)
        self.assertEqual(self.file_count + 1, files.count())

        file = files[self.file_count]
        self.assertEqual(self.barcode, file.barcode)
        self.assertEqual("wgs", file.format)
        self.assertGreater(file.entry_set.count(), 0)

    def tearDown(self):
        files = File.objects.filter(barcode=self.barcode)
        for file in files:
            file.delete()


class APIPostTestsInvalidBarcode(TestCase):
    barcode = 'fake_barcode'

    def setUp(self):
        self.api_results = upload(MagicMock(FILES=None, REQUEST={"barcode": self.barcode}))

    def test_correct_response_data(self):
        self.assertEqual(422, self.api_results.status_code)

        content = json.loads(self.api_results.content.decode("ascii"))

        self.assertEqual(self.barcode, content['barcode'])
        self.assertEqual('Invalid barcode', content['error'])

    def test_not_added_to_database(self):
        self.assertEqual(0, File.objects.filter(barcode=self.barcode).count())
