from django.test import TestCase

from basitapi.exception import ApiException

class ExceptionTest(TestCase):
    def test_init(self):
        exception = ApiException('Hata', 500, application_code=1000)
        self.assertEqual(exception.message, 'Hata')
        self.assertEqual(exception.status, 500)
        self.assertEqual(exception.application_code, 1000)
