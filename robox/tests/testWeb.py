import os
from unittest import skipIf

import mock
from django.core.urlresolvers import reverse
from django.db import IntegrityError, DatabaseError
from django.test import TransactionTestCase, LiveServerTestCase, TestCase
from selenium import webdriver

from mainsite import settings, environment
from robox.models import DataFile, Entry, MetaData, BinaryFile


class FileParseTestFail(TransactionTestCase):
    @mock.patch('robox.parsing.parse', return_value={'parser': "fake_parser", "data": [{'key': "value"}]})
    @mock.patch('robox.models.Entry.objects.create', side_effect=IntegrityError)
    def setUp(self, *save_mock):
        super(FileParseTestFail, self).setUp()

        try:
            with open(os.path.join(settings.BASE_DIR,
                                   "robox/tests/testfiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv"),
                      'rb') as f:
                self.file = DataFile.objects.create(barcode="fake_barcode",
                                                    binary_file=BinaryFile.objects.create(data=f.read(), name=str(f)))
            self.file.parse()
            self.exception = None
        except DatabaseError as err:
            self.exception = err

        self.file = DataFile.objects.get(pk=self.file.pk)

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


class FileParseTestSuccess(TransactionTestCase):
    @mock.patch('robox.parsing.parse', return_value={'parser': "fake_parser", "data": [{'key': "value"}]})
    def setUp(self, *save_mock):
        super(FileParseTestSuccess, self).setUp()

        try:
            with open(os.path.join(settings.BASE_DIR,
                                   "robox/tests/testFiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv"),
                      'rb') as f:
                self.file = DataFile.objects.create(barcode="fake_barcode",
                                                    binary_file=BinaryFile.objects.create(data=f.read(), name=str(f)))
            self.file.parse()
            self.exception = None
        except Exception as err:
            self.exception = err

        self.file = DataFile.objects.get(pk=self.file.pk)

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


@skipIf(not environment.CHROME_DRIVER, "Webdriver setting not set. Skipping.")
class UploadTestSuccess(LiveServerTestCase):
    barcode = "0000000000000"

    def setUp(self):
        self.driver = webdriver.Chrome(environment.CHROME_DRIVER)
        self.driver.get(self.live_server_url)

    def test_file_was_uploaded_and_parsed(self):
        self.driver.get(self.live_server_url + reverse('view', args=[self.barcode]))

        headers = self.driver.find_elements_by_class_name("file-header")
        contents = self.driver.find_elements_by_class_name("file-contents")

        self.assertEqual(0, len(headers), "Started with header already in barcode")
        self.assertEqual(0, len(contents), "Started with contents already in barcode")

        self.driver.find_element_by_link_text("Upload").click()

        self.driver.find_element_by_id("id_barcode").send_keys(self.barcode)
        self.driver.find_element_by_id("id_file").send_keys(
                os.path.join(settings.BASE_DIR,
                             "robox/tests/testFiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv")
        )

        self.driver.find_element_by_id('id_barcode').submit()

        headers = self.driver.find_elements_by_class_name("file-header")
        self.assertEqual(
                "File: Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv",
                headers[0].find_element_by_class_name('file-name').text)

        contents = self.driver.find_element_by_class_name("file-content")
        self.assertGreater(len(contents.find_elements_by_tag_name("tr")), 1)

    def tearDown(self):
        self.driver.quit()

        files = DataFile.objects.filter(barcode=self.barcode)
        for file in files:
            file.delete()


@skipIf(not environment.CHROME_DRIVER, "Webdriver setting not set. Skipping.")
class UploadTestInvalidBarcode(LiveServerTestCase):
    barcode = "0123456789123"

    def setUp(self):
        self.driver = webdriver.Chrome(environment.CHROME_DRIVER)
        self.driver.get(self.live_server_url)

        self.driver.find_element_by_link_text("Upload").click()
        self.upload_url = self.driver.current_url

        self.driver.find_element_by_id("id_barcode").send_keys(self.barcode)
        self.driver.find_element_by_id("id_file").send_keys(
                os.path.join(settings.BASE_DIR,
                             "robox/tests/testFiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv")
        )
        self.driver.find_element_by_id('id_barcode').submit()

    def test_still_on_upload_page(self):
        self.assertEqual(self.upload_url, self.driver.current_url)

    def test_file_upload_caused_error(self):
        errors = self.driver.find_elements_by_class_name("errorlist")
        self.assertEqual(1, len(errors))
        self.assertEqual("Invalid EAN13 barcode", errors[0].find_element_by_tag_name('li').text)

    def tearDown(self):
        self.driver.quit()


class DownloadFile(TestCase):
    def setUp(self):
        with open(os.path.join(settings.BASE_DIR,
                               "robox/tests/testFiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv"),
                  'rb') as f:
            self.file_data = f.read()
            self.file = DataFile.objects.create(barcode="fake_barcode",
                                                binary_file=BinaryFile.objects.create(data=self.file_data, name=str(f)))

    def test_download_returns_ok(self):
        url = reverse('download', args=[self.file.pk])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_file_contents(self):
        url = reverse('download', args=[self.file.pk])
        response = self.client.get(url)
        self.assertEqual(self.file_data, response.content)
