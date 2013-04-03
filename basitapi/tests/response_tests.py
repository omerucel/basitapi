from django.test import TestCase

from basitapi.response import ApiResponse
from basitapi.exception import ApiException

class ResponseTest(TestCase):
    def test_init(self):
        response = ApiResponse(content={'data': 1}, status=200)
        self.assertIsInstance(response.content, dict)
        self.assertEquals(response.to_object().data, 1)
        self.assertEqual(response.status, 200)

        try:
            ApiResponse(content="test", status=200)
            self.assertFalse(True)
        except ApiException,e:
            self.assertEquals(e.status, 500)
            self.assertEquals(e.message, "'content' must be of type dict.")

    def test_to_json(self):
        response = ApiResponse(content={'data':1}, status=200)
        self.assertEqual(response.to_json(), '{"data": 1}')

    def test_to_object(self):
        response = ApiResponse(content={'data':1}, status=200)
        self.assertEqual(response.to_object().data, 1)
