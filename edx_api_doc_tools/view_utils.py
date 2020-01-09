"""
Utilities for annotating API views with schema info.

External users: import these from __init__.
"""
from __future__ import absolute_import, unicode_literals

import six
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

from .internal_utils import dedent, split_docstring


def schema_for(method_name, docstring=None, **schema_kwargs):
    """
    Decorate a class to specify a schema for one of its methods.

    Useful when the method you are describing is not defined inside of your
    class body, but is instead defined somewhere up in the DRF view hierarchy.
    (For applying a schema directly to a method, use the `schema` decorator).

    DRF method names include:
        'list', 'retrieve', 'get',
        'post', 'create',
        'put', 'update',
        'patch', 'partial_update',
        'delete', and 'destroy'.

    The docstring of the specified method is replaced with `docstring`.
    If `docstring` is falsy, the class docstring is used.
    """
    def schema_for_inner(view_class):
        """
        Decorate a view class with the specified schema.
        """
        decorated_class = method_decorator(
            name=method_name,
            decorator=schema(**schema_kwargs),
        )(view_class)
        func_docstring = docstring or view_class.__doc__
        view_func = six.get_unbound_function(getattr(decorated_class, method_name))
        view_func.__doc__ = func_docstring
        return decorated_class
    return schema_for_inner


def schema(parameters=None, responses=None):
    """
    Decorate an API-endpoint-handling function to specify its schema.

    The operation summary and description are taken from the function docstring. All
    description fields should be in Markdown and will be automatically dedented.

    Args:
        parameters (list[openapi.Parameter]):
            Optional list of parameters to the API endpoint.
        responses (dict[int, object]):
            Optional map from HTTP statuses to either:
                * a serializer class corresponding to that status
                * a string describing when that status occurs
                * an openapi.Schema object
                * `None`, which indicates "don't include this response".
    """
    for param in parameters or ():
        param.description = dedent(param.description)

    # TODO: Remove this line when we drop Python 2 support.
    responses = _fix_responses_for_python_2(responses)

    def schema_inner(view_func):
        """
        Decorate a view function with the specified schema.
        """
        summary, description = split_docstring(view_func.__doc__)
        return swagger_auto_schema(
            manual_parameters=parameters,
            responses=responses,
            operation_summary=summary,
            operation_description=description,
        )(view_func)
    return schema_inner


def _fix_responses_for_python_2(responses):
    """
    Fix list of responses so that drf-yasg handles them correctly in Python 2.

    This is a temporary hack, necessary because drf-yasg doesn't explicitly support py2.

    Specifically, drf-yasg expects string response descriptions to be of type `str`,
    which in Py2, doesn't work on unicode strings.

    The offending line:
    github.com/axnsan12/drf-yasg/blob/1.17.0/src/drf_yasg/inspectors/view.py#L249

    TODO: Remove this function when we drop Python 2 support.

    Arguments:
        responses: dict[int, object]

    Returns: dict[int, object]
    """
    if six.PY3 or responses is None:
        return responses
    return {
        http_status: (
            value.encode('utf-8')
            if isinstance(value, unicode)  # pylint: disable=undefined-variable
            else value
        )
        for http_status, value in responses.iteritems()
    }


def is_schema_request(request):
    """
    Return whether this request serving an OpenAPI schema.
    """
    return request.query_params.get('format') == 'openapi'
