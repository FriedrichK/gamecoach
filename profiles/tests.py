from django.test import TestCase


class PlaceholderTestCase(TestCase):
    def setUp(self):
        self.test = 12

    def test_number_is_correct(self):
        self.assertEqual(self.test, 11)
