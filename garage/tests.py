from django.test import TestCase

# Create your tests here.
import garage.parsers

class Foo(TestCase):
    def test_stuff(self):
        print(garage.parsers.get_parsers())