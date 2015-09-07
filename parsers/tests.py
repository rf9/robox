from django.test import TestCase
import parsers

__author__ = 'rf9'


class ParserTest(TestCase):
    def test_parsers_have_been_added(self):
        self.assertGreater(len(parsers._PARSERS), 0)
