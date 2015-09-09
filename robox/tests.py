from django.db import IntegrityError, DatabaseError
from django.test import TransactionTestCase
import mock

from robox.models import File, Entry, MetaData


class TransactionTestRollBack(TransactionTestCase):
    @mock.patch('parsers.parsing.parse', return_value={'parser': "fake_parser", "data": ["data"]})
    @mock.patch('robox.models.Entry.objects.create', side_effect=IntegrityError)
    def setUp(self, *save_mock):
        super(TransactionTestRollBack, self).setUp()

        try:
            self.file = File.objects.create()
            self.file.parse()
            self.exception = None
        except DatabaseError as err:
            self.exception = err

        self.file.refresh_from_db()

    def test_that_file_was_created(self):
        self.assertIsNotNone(self.file)

    def test_that_format_was_not_set(self):
        self.assertEqual("None", self.file.format)

    def test_that_error_is_raised(self):
        self.assertIsNotNone(self.exception)

    def test_no_objects_were_created(self):
        self.assertEqual(0, Entry.objects.count())


class TransactionTestCommit(TransactionTestCase):
    @mock.patch('parsers.parsing.parse', return_value={'parser': "fake_parser", "data": [{'key': "value"}]})
    def setUp(self, *save_mock):
        super(TransactionTestCommit, self).setUp()
        self.file = File.objects.create()
        try:
            self.file.parse()
            self.exception = None
        except Exception as err:
            self.exception = err

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
