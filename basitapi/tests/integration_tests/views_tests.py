from django.test import TestCase
from django.utils import simplejson
from django.contrib.sessions.backends.db import SessionStore

from basitapi.views import ApiView
from basitapi.response import ApiResponse
from basitapi.exception import ApiException
from basitapi.decorators import check_session

from basitapi.tests.factories import UserFactory

class SampleView(ApiView):
    def get(self, request):
        return ApiResponse({
            'method' : 'get',
            'data' : int(request.REQUEST.get('data', 0))
        })

    def post(self, request):
        return ApiResponse({
            'method' : 'post',
            'data' : int(request.REQUEST.get('data', 0))
        })

    def delete(self, request):
        return ApiResponse({
            'method' : 'delete',
            'data' : int(request.REQUEST.get('data', 0))
        })

    def put(self, request):
        return ApiResponse({
            'method' : 'put',
            'data' : int(request.REQUEST.get('data', 0))
        })

class SampleErrorView(ApiView):
    def get(self, request):
        raise ApiException('Hata - GET', status=401, application_code=50)

    def put(self, request):
        raise ApiException('Hata - PUT', status=401, application_code=50)

    def delete(self, request):
        return ApiResponse({
            'ok' : ok
        })

class SampleSessionView(ApiView):
    @check_session
    def get(self, request):
        return ApiResponse({
            'user_id' : request.user.id,
            'session_key' : request.session_store.session_key
        })

class ViewTest(TestCase):
    urls = 'basitapi.tests.urls'

    def test_200_response(self):
        response = self.client.get('/sample')
        self.assertEquals(response.status_code, 200)

        response = self.client.post('/sample')
        self.assertEquals(response.status_code, 200)

        response = self.client.delete('/sample')
        self.assertEquals(response.status_code, 200)

        response = self.client.put('/sample')
        self.assertEquals(response.status_code, 200)

    def test_error_response(self):
        response = self.client.get('/error')
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('message'), 'Hata - GET')
        self.assertEquals(data.get('status'), 401)
        self.assertEquals(data.get('application_code'), 50)
        self.assertEquals(response.status_code, 401)

        response = self.client.put('/error')
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('message'), 'Hata - PUT')
        self.assertEquals(data.get('status'), 401)
        self.assertEquals(data.get('application_code'), 50)

        response = self.client.delete('/error')
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('message'), 'Internal Server Error')
        self.assertEquals(data.get('status'), 500)

    def test_data_response(self):
        response = self.client.get('/sample', {'data':123})
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('data'), 123)

        response = self.client.post('/sample', {'data': 234})
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('data'), 234)

        response = self.client.put('/sample', '{"data": 567}', content_type='application/x-www-form-urlencoded')
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('data'), 567)

        response = self.client.delete('/sample?data=891')
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('data'), 891)

    def test_content_type(self):
        response = self.client.get('/sample.json')
        self.assertEquals(response._headers['content-type'][1], 'application/json; charset=utf-8');

        response = self.client.get('/sample.xml')
        self.assertEquals(response._headers['content-type'][1], 'text/xml; charset=utf-8');

    def test_session(self):
        response = self.client.get('/session.json')
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('message'), 'Unauthorized')
        self.assertEquals(data.get('status'), 401)

        user_one = UserFactory.create()

        session_store = SessionStore()
        session_store['_auth_user_id'] = user_one.id
        session_store['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
        session_store.save()


        response = self.client.get('/session', {'session_key' : session_store.session_key})
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('user_id'), user_one.id)
        self.assertEquals(data.get('session_key'), session_store.session_key)

        session_store = SessionStore()
        session_store['_auth_user_id'] = 3
        session_store['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
        session_store.save()

        response = self.client.get('/session', {'session_key' : session_store.session_key})
        data = simplejson.loads(response.content)
        self.assertEquals(response.status_code, 401)
        self.assertEquals(data.get('status'), 401)


    def test_suppress_response_code(self):
        response = self.client.get('/error.json', {'suppress_response_codes':1})
        data = simplejson.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data.get('message'), 'Hata - GET')
        self.assertEquals(data.get('status'), 401)

    def test_inject_method(self):
        response = self.client.post('/sample.json', {'method' : 'get'})
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('method'), 'get')

    def test_unsupported_format(self):
        response = self.client.get('/sample.html')
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('message'), 'Unsupported response format.')

    def test_http_accept(self):
        response = self.client.get('/sample', {'data' : 345}, HTTP_ACCEPT='application/json')
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('data'), 345)

    def test_method_not_allowed(self):
        response = self.client.post('/error')
        data = simplejson.loads(response.content)
        self.assertEquals(data.get('status'), 405)
