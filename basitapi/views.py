#-*- coding: utf-8 -*-

import django

from django.utils import simplejson
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, QueryDict

#from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException

from basitapi.exception import ApiException
from basitapi.response import ApiResponse

class ApiView(View):
    """
    View sınıflarına Api desteği kazandırır.
    """

    _format = None

    def http_method_not_allowed(self, request, *args, **kwargs):
        raise ApiException('Method not allowed.',405)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        """
        Gelen istek application/x-www-form-urlencoded ile gönderilmişse
        raw_post_data içindeki veriler objeye çevrilir ve request.REQUEST güncellenir.
        """

        if django.VERSION[0] >= 1 and django.VERSION[1] > 4:
            request_body = request.body
        else:
            request_body = request.raw_post_data

        if 'application/x-www-form-urlencoded' in request.META.get('CONTENT_TYPE', '') and request.method in ['PUT']:
            request.REQUEST.dicts = (request.POST, request.GET, simplejson.loads(request_body))

        if 'application/json' in request.META.get('CONTENT_TYPE', ''):
            request.REQUEST.dicts = (request.POST, request.GET, simplejson.loads(request_body))

        try:
            # Yanıt formatını belirlemek için önce HTTP_ACCEPT kontrol ediliyor.
            if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                self._format = 'json'
            else:
                # Bağlantı son ekine göre format belirleniyor.
                self._format = kwargs.get('format', 'json')

                # Destek verilmeyen format isteklerinde hata görüntüle.
                if self._format not in ['json', 'xml']:
                    raise ApiException('Unsupported response format.', 400)

            # format parametrelerden temizleniyor. Boş yere kalabalık olmasın..
            if kwargs.has_key('format'):
                del kwargs['format']

            # method parametresi ile istek yapılırsa ilgili metodun çalıştırılması sağlanıyor. (method=PUT, method=POST vb.)
            # Diğer durumlar için View sınıfının dispatch metodu kullanılır.
            if request.REQUEST.get('method', '').lower() in self.http_method_names:
                handler = getattr(self, request.REQUEST.get('method').lower(), self.http_method_not_allowed)
            else:
                handler = super(ApiView, self).dispatch

            response = handler(request, *args, **kwargs)
        except ApiException, error:
            data = {
                'message' : error.message,
                'status' : error.status
            }

            if not error.application_code == None:
                data.update({'application_code' : error.application_code})

            response = ApiResponse(data, error.status)
        except Exception, error:
            response = ApiResponse({
                'message' : 'Internal Server Error',
                'status' : 500
            }, 500)
        finally:
            # TODO : Yanıtın farklı formatlarda sunulabilmesini destekle
            if isinstance(response, ApiResponse):
                status_code = response.status
                mimetype = 'text/plain'
                if self._format == 'json':
                    mimetype = 'application/json'
                elif self._format == 'xml':
                    mimetype = 'text/xml'

                response = HttpResponse(response.to_json(), '%s; charset=utf-8' %(mimetype))
                response.status_code = status_code

            # İstemci tarafındaki yetersizliklerden dolayı bazen 200 haricindeki hata kodları soruna neden olabiliyor.
            # Bu sorunu aşmak için suppress_response_codes=1 değeri ile istekte bulunmak yeterli.
            if request.GET.get('suppress_response_codes', False) == '1':
                response.status_code = 200

            return response

