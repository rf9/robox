import os

from django.core.files.uploadedfile import UploadedFile
from django.db import IntegrityError, DatabaseError
from django.test import TransactionTestCase
import mock

from mainsite import settings

from robox.models import File, Entry, MetaData


class TransactionTestRollBack(TransactionTestCase):
    @mock.patch('parsing.parse', return_value={'parser': "fake_parser", "data": [{'key': "value"}]})
    @mock.patch('robox.models.Entry.objects.create', side_effect=IntegrityError)
    def setUp(self, *save_mock):
        super(TransactionTestRollBack, self).setUp()

        try:
            with open(os.path.join(settings.BASE_DIR,
                                   "parsing/testFiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv"),
                      'rb') as f:
                self.file = File.objects.create(barcode="fake_barcode", file=UploadedFile(file=f))
            self.file.parse()
            self.exception = None
        except DatabaseError as err:
            self.exception = err

        self.file = File.objects.get(pk=self.file.pk)

    def test_that_file_was_created(self):
        self.assertIsNotNone(self.file)

    def test_that_format_was_not_set(self):
        self.assertEqual("None", self.file.format)

    def test_that_error_is_raised(self):
        self.assertIsNotNone(self.exception)

    def test_no_objects_were_created(self):
        self.assertEqual(0, Entry.objects.count())

    def tearDown(self):
        self.file.delete()


class TransactionTestCommit(TransactionTestCase):
    @mock.patch('parsing.parse', return_value={'parser': "fake_parser", "data": [{'key': "value"}]})
    def setUp(self, *save_mock):
        super(TransactionTestCommit, self).setUp()

        try:
            with open(os.path.join(settings.BASE_DIR,
                                   "parsing/testFiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv"),
                      'rb') as f:
                self.file = File.objects.create(barcode="fake_barcode", file=UploadedFile(file=f))
            self.file.parse()
            self.exception = None
        except Exception as err:
            self.exception = err

        self.file = File.objects.get(pk=self.file.pk)

    def test_that_file_was_created(self):
        self.assertIsNotNone(self.file)

    def test_that_format_was__set(self):
        self.assertEqual("fake_parser", self.file.format)

    def test_that_no_errors_are_raised(self):
        self.assertIsNone(self.exception)

    def test_entry_was_created(self):
        self.assertEqual(1, Entry.objects.count())

    def test_meta_data_was_created(self):
        self.assertEqual(1, MetaData.objects.count())
        data = MetaData.objects.all()[0]
        self.assertEqual("key", data.key)
        self.assertEqual('value', data.value)

    def tearDown(self):
        self.file.delete()
