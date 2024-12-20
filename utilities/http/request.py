from datetime import datetime

from django.utils.functional import cached_property
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request

from utilities.http.exceptions import APIExceptionWithMetadata


class MandatoryFieldException(APIExceptionWithMetadata):
    def __init__(self, field_name, detail=None, required_data_type=None):
        super().__init__(
            status_code=400, code=ValidationError.default_code, detail=detail
            or ValidationError.default_detail, metadata={
                'field_name': field_name,
                'required_data_type': str(required_data_type)
            })


class RequestWrapperMixin:
    @cached_property
    def wrapper(self):
        """:rtype: RequestWrapper"""
        return RequestWrapper(self.request)


class RequestBodyWrapper:
    def __init__(self, request_body):
        self.body = request_body

    def get_date_param(self, field_name, mandatory=True):
        try:
            string_value = self.body[field_name]
            return datetime.strptime(string_value, '%Y-%m-%d').date()
        except Exception:
            if not mandatory:
                return None
            raise MandatoryFieldException(
                field_name, 'A date field is missing or malformed, the right format is %Y-%m-%d')

    def get_param(self, field_name, data_type=None, mandatory=True):
        def extract():
            if field_name not in self.body:
                return None
            if data_type is None:
                return self.body[field_name]
            if not isinstance(self.body[field_name], data_type):
                return None
            return data_type(self.body[field_name])

        result = extract()
        if result is None and mandatory:
            raise MandatoryFieldException(field_name, required_data_type=data_type)
        return result


class RequestWrapper:
    def __init__(self, request):
        self.request = request
        try:
            self._request_body_wrapper = RequestBodyWrapper(request.data)
        except AttributeError:
            self._request_body_wrapper = RequestBodyWrapper({})

    def get_access_mode(self):
        return self.request.META.get('HTTP_ACCESS_MODE', None)

    def get_header(self, header_key):
        meta = self.request.META
        if header_key in meta:
            return meta.get(header_key)
        return meta.get('HTTP_{key}'.format(key=header_key.upper()))

    def get_user(self):
        return self.request.user

    def get_entity_id(self):
        try:
            return int(self.request.META['HTTP_ENTITY_ID'])
        except (KeyError, ValueError):
            return None

    def get_query_param(self, field_name, mandatory=True):
        """
        :exception MandatoryFieldException
        :return: value of the field
        """
        value = self.request.GET.get(field_name, None)
        if value is None:
            if not mandatory:
                return None
            raise MandatoryFieldException(field_name)
        return value

    def get_date_body_param(self, field_name, mandatory=True):
        return self._request_body_wrapper.get_date_param(field_name, mandatory=mandatory)

    def get_date_query_param(self, field_name, default_str=None, mandatory=True):
        def generate_date():
            string_value = self.request.GET.get(field_name, default_str)
            if not string_value:
                return None
            try:
                return datetime.strptime(string_value, '%Y-%m-%d').date()
            except ValueError:
                return None

        result = generate_date()
        if not result and mandatory:
            raise MandatoryFieldException(
                field_name, 'A date field is missing or malformed, the right format is %Y-%m-%d')
        return result

    def get_from_date_query_param(self, field_name='from_date', default_str=None, mandatory=True):
        return self.get_date_query_param(field_name, default_str, mandatory=mandatory)

    def get_to_date_query_param(self, field_name='to_date', default_str=None, mandatory=True):
        try:
            return self.get_date_query_param(field_name, default_str, mandatory=mandatory)
        except (ValueError, TypeError):
            return None

    def get_query_param_as_int(self, field_name, mandatory=True):
        """
        :exception MandatoryFieldException
        :return: value of the field
        """
        def extract_as_int():
            value = self.get_query_param(field_name, mandatory=mandatory)
            try:
                return int(value)
            except ValueError:
                return None
            except TypeError:
                return None

        result = extract_as_int()
        if result is None and mandatory:
            raise MandatoryFieldException(field_name, required_data_type=int)
        return result

    def get_query_param_as_bool(self, field_name, mandatory=True):
        """
        :exception MandatoryFieldException
        :return: value of the field
        """
        def extract_as_bool():
            value = self.get_query_param(field_name, mandatory=mandatory)
            try:
                value = eval(value)
            except NameError:
                return None
            except TypeError:
                return None
            if not isinstance(value, bool):
                return None
            return value

        result = extract_as_bool()
        if result is None and mandatory:
            raise MandatoryFieldException(field_name, required_data_type=bool)
        return result

    def get_body_param(self, field_name, data_type=None, mandatory=True):
        return self._request_body_wrapper.get_param(field_name, data_type=data_type,
                                                    mandatory=mandatory)


def get_request_ip(request: Request) -> str:
    return request.META.get('HTTP_X_REAL_IP')
