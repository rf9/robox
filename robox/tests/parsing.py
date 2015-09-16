import os

from django.test import TestCase

from mainsite import settings

from robox.parsing import _PARSERS

__author__ = 'rf9'


class ParserTest(TestCase):
    def test_parsers_have_been_added(self):
        self.assertGreater(len(_PARSERS), 0)


class AbstractClasses:
    class ParserTestMixin(TestCase):
        def setUp(self):
            try:
                self.accepts = self.parser.accept(self.accepted_file)
                self.parsed_data = list(self.parser.parse(self.accepted_file))
                self.exception = None
            except Exception as err:
                self.exception = err

        def test_accepts_file(self):
            self.assertTrue(self.accepts)

        def test_no_exceptions_raised(self):
            self.assertIsNone(self.exception)

        def test_parsed_data_has_correct_headings(self):
            headings = {key for entry in self.parsed_data for key in entry}

            self.assertEqual(sorted(headings), self.expected_headings)

        def test_parsed_data_is_correct(self):
            for index, (actual_entry, expected_entry) in enumerate(zip(self.parsed_data, self.expected_data)):
                self.assertEqual(expected_entry, actual_entry, msg="Line " + str(index))


class IscParserTest(AbstractClasses.ParserTestMixin):
    def setUp(self):
        self.parser = _PARSERS['isc']
        file_path = os.path.join(settings.BASE_DIR,
                                 "robox/tests/testFiles/Caliper2_402755_ISC_1_5_2015-06-30_07-44-47_WellTable.csv")
        with open(file_path, 'r') as fin:
            self.accepted_file = [bytes(line, encoding='ascii') for line in fin]
        self.expected_headings = ['address', 'name', 'units', 'value']
        self.expected_data = [{'address': 'A1', 'units': 'nM', 'name': 'concentration', 'value': '5.25554636996337'},
                              {'address': 'A1', 'name': 'dilution', 'units': '%', 'value': 20.0},
                              {'address': 'A1', 'units': 'nM', 'name': 'concentration', 'value': '5.26363880140032'},
                              {'address': 'A1', 'name': 'dilution', 'units': '%', 'value': 20.0},
                              {'address': 'B1', 'units': 'nM', 'name': 'concentration', 'value': '8.76213326868774'},
                              {'address': 'B1', 'name': 'dilution', 'units': '%', 'value': 20.0},
                              {'address': 'B1', 'units': 'nM', 'name': 'concentration', 'value': '8.69241398098586'},
                              {'address': 'B1', 'name': 'dilution', 'units': '%', 'value': 20.0}]

        super(IscParserTest, self).setUp()


class WgsParserTest(AbstractClasses.ParserTestMixin):
    def setUp(self):
        self.parser = _PARSERS['wgs']
        file_path = os.path.join(settings.BASE_DIR,
                                 "robox/tests/testfiles/Caliper1_411359_PATH_1_3_2015-08-18_01-24-42_WellTable.csv")
        with open(file_path, 'r') as fin:
            self.accepted_file = [bytes(line, encoding='ascii') for line in fin]
        self.expected_headings = ['address', 'name', 'units', 'value']
        self.expected_data = [{'address': 'A1', 'units': 'nM', 'name': 'concentration', 'value': '0.798277646077084'},
                              {'address': 'A1', 'name': 'dilution', 'units': '%', 'value': 33.33333333333333},
                              {'address': 'A1', 'units': 'nM', 'name': 'concentration', 'value': '0.768245464273193'},
                              {'address': 'A1', 'name': 'dilution', 'units': '%', 'value': 33.33333333333333},
                              {'address': 'B1', 'units': 'nM', 'name': 'concentration', 'value': '0.899607410537338'},
                              {'address': 'B1', 'name': 'dilution', 'units': '%', 'value': 33.33333333333333},
                              {'address': 'B1', 'units': 'nM', 'name': 'concentration', 'value': '0.866752116160426'},
                              {'address': 'B1', 'name': 'dilution', 'units': '%', 'value': 33.33333333333333}, ]

        super(WgsParserTest, self).setUp()


class XTenParserTest(AbstractClasses.ParserTestMixin):
    def setUp(self):
        self.parser = _PARSERS['xTen']
        self.accepted_file = os.path.join(settings.BASE_DIR,
                                          "robox/tests/testfiles/DN_DSS1_BR_PCRXP_Assay.xlsx")
        self.expected_headings = ['address', 'name', 'units', 'value']
        self.expected_data = [{'address': 'A1', 'name': 'concentration', 'units': 'ng/ul', 'value': 20.393},
                              {'address': 'B1', 'name': 'concentration', 'units': 'ng/ul', 'value': 26.737},
                              {'address': 'C1', 'name': 'concentration', 'units': 'ng/ul', 'value': 22.707},
                              {'address': 'D1', 'name': 'concentration', 'units': 'ng/ul', 'value': 22.389}]

        super(XTenParserTest, self).setUp()