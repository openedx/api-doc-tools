"""
Utilities for annotating API views with schema info.

External users: import these from __init__.
"""
from __future__ import absolute_import, unicode_literals

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet

from .internal_utils import dedent, split_docstring


def schema_for(method_name, docstring=None, **schema_kwargs):
    """
    Decorate a class to specify a schema for one of its methods.

    Useful when the method you are describing is not defined inside of your
    class body, but is instead defined somewhere up in the DRF view hierarchy.
    (For applying a schema directly to a method, use the :func:`.schema`
    decorator).

    DRF method names include: ``list``, ``retrieve``, ``get``, ``post``,
    ``create``, ``put``, ``update``, ``patch``, ``partial_update``,
    ``delete``, and ``destroy``.

    Arguments:
        method_name (str): Name of the method to decorate.
        docstring (str): Optional summary and description of the operation,
            which takes the same format that :func:`.schema` expects of function
            docstrings (that is, a summary line, followed by a newline,
            followed by one or more lines of description).
        **schema_kwargs: kwargs to pass to :func:`.schema`.
    """
    def schema_for_inner(view_class):
        """
        Decorate a view class with the specified schema.
        """
        summary, description = split_docstring(docstring)
        decorated_class = method_decorator(
            name=method_name,
            decorator=schema(
                summary=summary, description=description, **schema_kwargs
            ),
        )(view_class)
        return decorated_class
    return schema_for_inner


def exclude_schema_for(*method_names):
    """
    Decorate a class to exlcude one or more of of its methods from the API docs.

    Arguments:
        method_names (list[str]): Names of view methods whose operations will be
            excluded from the generated API documentation.

    Example::

        @schema_for('get', ...)
        @schema_for('delete', ...)
        @exclude_schema_for('put', 'patch')
        class MyView(RetrieveUpdateDestroyAPIView):
            pass
    """
    def exclude_schema_for_inner(view_class):
        """
        Decorate a view class to exclude specified methods.
        """
        for method_name in method_names:
            method_decorator(
                name=method_name, decorator=exclude_schema
            )(view_class)
        return view_class
    return exclude_schema_for_inner


def exclude_schema_for_all(view_class):
    """
    Decorate a class to exlcude all of its methods from the API docs.

    Arguments:
        view_class (type): A type, typically a subclass of View or ViewSet.

    Example::

        @exclude_schema_for_all
        class MyView(RetrieveUpdateDestroyAPIView):
            pass
    """
    all_viewset_api_methods = {
        'list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'
    }
    all_view_api_methods = {
        'get', 'post', 'put', 'patch', 'delete'
    }
    is_viewset = issubclass(view_class, ViewSet)
    all_api_methods = all_viewset_api_methods if is_viewset else all_view_api_methods
    methods_to_exclude = {
        method for method in all_api_methods if hasattr(view_class, method)
    }
    return exclude_schema_for(*methods_to_exclude)(view_class)


def schema(
    parameters=None,
    responses=None,
    summary=None,
    description=None,
):
    """
    Decorate an API-endpoint-handling function to specify its schema.

    The operation summary and description are taken from the function docstring. All
    description fields should be in Markdown and will be automatically dedented.

    Arguments:
        parameters (list[openapi.Parameter]): Optional list of parameters to
            the API endpoint.
        responses (dict[int, object]): Optional map from HTTP statuses to either:
            * a serializer class corresponding to that status
            * a string describing when that status occurs
            * an openapi.Schema object
            * `None`, which indicates "don't include this response".
        summary (str): One-line summary of operation.
            If None, we attempt to extract it from the first line of the docstring.
        description (str): Optional multi-line description of operation.
            If None, we attempt to extract it from the rest of the docstring.
    """
    for param in parameters or ():
        param.description = dedent(param.description)

    def schema_inner(view_func):
        """
        Decorate a view function with the specified schema.
        """
        docstring_summary, docstring_description = split_docstring(view_func.__doc__)
        final_summary = summary or docstring_summary
        final_description = description or docstring_description or final_summary
        return swagger_auto_schema(
            manual_parameters=parameters,
            responses=responses,
            operation_summary=final_summary,
            operation_description=final_description,
        )(view_func)
    return schema_inner


def exclude_schema(view_func):
    """
    Decorate an API-endpoint-handling function to exclude it from the API docs.

    Example::

        class MyView(APIView):

            @schema(...)
            def get(...):
                pass

            @exclude_schema
            def post(...):
                pass
    """
    return swagger_auto_schema(auto_schema=None)(view_func)


def is_schema_request(request):
    """
    Return whether this request is serving an OpenAPI schema.
    """
    return request.query_params.get('format') == 'openapi'
