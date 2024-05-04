from django.http import HttpResponse

from utilities.exceptions import BusinessLogicException, UnexpectedEventException


class ApplicationExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except BusinessLogicException as e:
            return HttpResponse(e.detail)
        except UnexpectedEventException as e:
            return HttpResponse(e.detail)
