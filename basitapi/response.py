#-*- coding: utf-8 -*-

"""
Api yanıtı ile ilgili sınıf ve fonksiyonları içerir.
"""

from django.utils import simplejson

class ApiResponse:
    """
    API yanıtlarının taşınması için kullanılır. Yanıtın düzgün bir şekilde 
    istenilen formata çevirir.
    """
    @staticmethod
    def okay(content=None):
        """
        HTTP 200 status code
        """
        return ApiResponse(content, status=200)

    @staticmethod
    def created(content=None):
        """
        HTTP 201 status code
        """
        return ApiResponse(content, status=201)

    @staticmethod
    def accepted(content=None):
        """
        HTTP 202 status code
        """
        return ApiResponse(content, status=202)

    @staticmethod
    def bad_request(content=None):
        """
        HTTP 400 status code
        """
        return ApiResponse(content, status=400)

    @staticmethod
    def unauthorized(content=None):
        """
        HTTP 401 status code
        """
        return ApiResponse(content, status=401)

    @staticmethod
    def payment_required(content=None):
        """
        HTTP 402 status code
        """
        return ApiResponse(content, status=402)

    @staticmethod
    def forbidden(content=None):
        """
        HTTP 403 status code
        """
        return ApiResponse(content, status=403)

    @staticmethod
    def not_found(content=None):
        """
        HTTP 404 status code
        """
        return ApiResponse(content, status=404)

    @staticmethod
    def method_not_allowed(content=None):
        """
        HTTP 405 status code
        """
        return ApiResponse(content, status=405)

    def __init__(self, content=None, status=200):
        if content == None:
            content = {}

        self.content = content
        self.status = status

    def to_json(self):
        """
        Yanıt içeriğini json formatına çevirir.
        """
        return simplejson.dumps(self.content)

    def to_object(self):
        """
        Yanıt içeriğini objeye dönüştürür.
        """
        class Object:
            """
            Temp object
            """
            def __init__(self, kwargs):
                for i in kwargs:
                    setattr(self, i, kwargs[i])

        obj = Object(self.content)
        return obj
