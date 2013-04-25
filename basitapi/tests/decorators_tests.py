from django.test import TestCase
from django.contrib.auth.models import User

from basitapi.decorators import load_model
from basitapi.tests import factories

class DecoratorsTest(TestCase):
    def test_load_model(self):
        user = factories.UserFactory()

        class TempObject:
            @load_model(model=User, id_name='user_id', access_name='user')
            def temp_method(self, request, user_id):
                print request
                return request.user.id

        class TempData:
            def __init__(self):
                pass

        temp_object = TempObject()
        self.assertEquals(user.id, temp_object.temp_method(TempData(), user_id=user.id))

        self.assertEquals(404, temp_object.temp_method(TempData(), user_id=123123123).status)
