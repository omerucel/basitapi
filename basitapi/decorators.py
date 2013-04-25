#-*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from basitapi.response import ApiResponse

def load_model(model, id_name, access_name):
    def decorator(func):
        def wrapped(self, request, *args, **kwargs):
            if kwargs.has_key(id_name):
                try:
                    setattr(request, access_name, model.objects.get(id=kwargs[id_name]))
                except ObjectDoesNotExist:
                    return ApiResponse.not_found()

            return func(self, request, *args, **kwargs)

        return wrapped
    return decorator
