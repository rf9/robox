from ast import literal_eval
import json
import os

from django.core.urlresolvers import reverse
from django.test import TestCase
import mock

from mainsite import settings
from robox.models import DataFile, BinaryFile


class APIGetTests(TestCase):
    barcode = "0000000000000"

    def setUp(self):
        with open(os.path.join(settings.BASE_DIR,
                               "robox/tests/testfiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv"),
                  'rb') as f:
            self.file = DataFile.objects.create(barcode=self.barcode,
                                                binary_file=BinaryFile.objects.create(data=f.read(), name=str(f)))
        self.file.parse()
        self.file.refresh_from_db()

    def test_with_valid_barcode(self):
        url = reverse('file-list') + "?barcode=" + self.barcode
        api_results = self.client.get(url)

        self.assertEqual(200, api_results.status_code)
        results = json.loads(api_results.content.decode("ascii"))['results']

        self.assertEqual(1, len(results))
        content = results[0]

        self.assertEqual(self.barcode, content["barcode"])
        self.assertIn('data', content)
        self.assertEqual(375, len(content['data']))
        self.assertIn('upload_time', content)
        self.assertIn('format', content)

    def test_with_invalid_barcode(self):
        url = reverse('file-list') + "?barcode=fakebarcode"
        api_results = self.client.get(url)

        self.assertEqual(200, api_results.status_code)
        results = json.loads(api_results.content.decode("ascii"))['results']

        self.assertEqual(0, len(results))


def mock_return(value):
    for file in value['files']:
        file['file'] = 'mock_file_path'
        file['upload_time'] = "upload_time"

    return str(value)


class APIPostTestsValidBarcode(TestCase):
    barcode = "0000000000000"

    @mock.patch('django_extensions.db.fields.json.dumps', side_effect=mock_return)
    def setUp(self, *save_mock):
        self.file_count = DataFile.objects.filter(barcode=self.barcode).count()

        with open(os.path.join(settings.BASE_DIR,
                               "robox/tests/testfiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv"),
                  'rb') as f:
            url = reverse('file-list')
            data = {"barcode": self.barcode, "uploaded_file": f}
            self.api_results = self.client.post(url, data=data)

    def test_correct_response_data(self):
        self.assertEqual(201, self.api_results.status_code)
        response = literal_eval(self.api_results.content.decode("ascii"))

        self.assertIn('results', response)
        self.assertEqual(1, len(response['results']))
        content = response['results'][0]

        self.assertEqual(self.barcode, content["barcode"])
        self.assertIn('data', content)
        self.assertEqual(375, len(content['data']))
        self.assertIn('upload_time', content)
        self.assertIn('format', content)
        self.assertEqual("wgs", content['format'])

    def test_file_added_to_database(self):
        files = DataFile.objects.filter(barcode=self.barcode)
        self.assertEqual(self.file_count + 1, files.count())

        file = files[self.file_count]
        self.assertEqual(self.barcode, file.barcode)
        self.assertEqual("wgs", file.format)
        self.assertGreater(file.entry_set.count(), 0)


class APIPostTestMultipleFiles(TestCase):
    barcode = "0000000000000"

    @mock.patch('django_extensions.db.fields.json.dumps', side_effect=mock_return)
    def setUp(self, *save_mock):
        self.file_count = DataFile.objects.filter(barcode=self.barcode).count()

        with open(os.path.join(settings.BASE_DIR,
                               "robox/tests/testfiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv"),
                  'rb') as f1:
            with open(os.path.join(settings.BASE_DIR,
                                   "robox/tests/testfiles/Caliper2_402755_ISC_1_5_2015-06-30_07-44-47_WellTable.csv"),
                      'rb') as f2:
                url = reverse('file-list')
                data = {"barcode": self.barcode, "uploaded_file1": f1, "uploaded_file2": f2}
                self.api_results = self.client.post(url, data=data)

    def test_correct_response_data(self):
        self.assertEqual(201, self.api_results.status_code)
        response = literal_eval(self.api_results.content.decode("ascii"))

        self.assertIn('results', response)
        self.assertEqual(2, len(response['results']))

        for content in response['results']:
            self.assertEqual(self.barcode, content["barcode"])
            self.assertIn('data', content)
            self.assertIn('upload_time', content)
            self.assertIn('format', content)

        entries = [len(content['data']) for content in response['results']]
        formats = [content['format'] for content in response['results']]
        self.assertListEqual([375, 384], sorted(entries))
        self.assertListEqual(['isc', 'wgs'], sorted(formats))

    def test_file_added_to_database(self):
        files = DataFile.objects.filter(barcode=self.barcode)
        self.assertEqual(self.file_count + 2, files.count())

        for file in files[self.file_count:self.file_count + 1]:
            self.assertEqual(self.barcode, file.barcode)
            self.assertIn(file.format, ['wgs', 'isc'])
            self.assertGreater(file.entry_set.count(), 300)


class APIPostTestsInvalidBarcode(TestCase):
    barcode = '0000000000001'

    def setUp(self):
        url = reverse('file-list')
        data = {"barcode": self.barcode}
        self.api_results = self.client.post(url, data=data)

    def test_correct_response_data(self):
        self.assertEqual(422, self.api_results.status_code)

        content = json.loads(self.api_results.content.decode("ascii"))

        self.assertEqual(self.barcode, content['barcode'])
        self.assertEqual('Invalid barcode', content['error'])

    def test_not_added_to_database(self):
        self.assertEqual(0, DataFile.objects.filter(barcode=self.barcode).count())
