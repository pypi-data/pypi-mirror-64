from functools import wraps

from power_dict.schema_validator import SchemaValidator
from rest_framework.exceptions import APIException

from drf_toolkit.drf_utils import DrfUtils


def validate_request(schema):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, *args, **kwargs):
            request = view.request
            context = DrfUtils.get_request_parameters(request)
            context = DrfUtils.transform_list_parameters(context, schema)

            context = SchemaValidator.validate(context, schema)
            kwargs['context'] = context
            return view_func(view, *args, **kwargs)

        return _wrapped_view

    return decorator


def except_error():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, *args, **kwargs):
            try:
                return view_func(view, *args, **kwargs)
            except APIException as ex:
                raise ex
            except Exception as ex:
                return DrfUtils.generate_bad_response(exception=ex)

        return _wrapped_view

    return decorator
