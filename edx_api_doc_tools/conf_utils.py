"""
Functions for setting up API doc generation & viewing in a repository.

External users: import these from __init__.
"""

from django.conf import settings
from django.urls import path, re_path
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def make_docs_urls(api_info, api_url_patterns=None):
    """
    Create API doc views given an API info object.

    Arguments:
        api_info (openapi.Info): Information about the API.
        api_url_patterns (list of url patterns): URL patterns that API docs will be generated for

    Returns: list[RegexURLPattern]
        A list of url patterns to the API docs.

    Example::

        # File: urls.py
        from edx_api_doc_tools import make_docs_urls, make_api_info
        urlpatterns = [ ... ] # Your URL patterns.
        api_info = make_api_info(title="Awesome API", version="v42")
        urlpatterns += make_docs_urls(api_info)
    """
    return get_docs_urls(
        docs_data_view=make_docs_data_view(api_info, api_url_patterns),
        docs_ui_view=make_docs_ui_view(api_info, api_url_patterns),
    )


def make_api_info(
        title="Open edX APIs",
        version="v1",
        email="oscm@edx.org",
        description="APIs for access to Open edX information",
):
    """
    Build an API info object.

    Arguments:
        title (str): The title of the API.
        version (str): The version of the API.
        email (str): Contact email address for API support or questions.
        description (str): Description of the API.

    Returns: openapi.Info
    """
    return openapi.Info(
        title=title,
        default_version=version,
        contact=openapi.Contact(email=email),
        description=description,
    )


def get_docs_urls(docs_data_view, docs_ui_view):
    """
    Get some reasonable URL patterns to browsable API docs and API docs data.

    If these URL patterns don't work for your service,
    feel free to construct your own.

    Arguments:
        docs_data_view (openapi.Info): JSON/YAML view for API docs data.
        docs_ui_view (openapi.Info): Nice HTML view for API docs.

    Returns: list[RegexURLPattern]
        A list of url patterns to the API docs.

    Example::

        # File: urls.py
        from edx_api_doc_tools import get_docs_urls
        from .views import custom_doc_data_view, custom_doc_ui_view
        urlpatterns = [ ... ] # Your URL patterns.
        urlpatterns += get_docs_urls(custom_doc_data_view, custom_doc_ui_view)
    """
    return [
        re_path(
            r'^swagger(?P<format>\.json|\.yaml)$',
            docs_data_view,
            name='apidocs-data',
        ),
        path('api-docs/', docs_ui_view,
             name='apidocs-ui',
             ),
        path('swagger/', RedirectView.as_view(pattern_name='apidocs-ui', permanent=False),
             name='apidocs-ui-swagger',
             ),
    ]


def make_docs_data_view(api_info, api_url_patterns=None):
    """
    Build View for API documentation data (either JSON or YAML).

    Arguments:
        api_info (openapi.Info): Information about the API.
        api_url_patterns (list of url patterns): URL patterns that API docs will be generated for

    Returns: View

    Example::

        from edx_api_doc_tools import make_api_info, make_docs_data_view
        api_info = make_api_info(title="Awesome API", version="v42")
        my_data_view = make_docs_data_view(api_info)
    """
    schema_generator = get_schema_generator(api_url_patterns)

    return get_schema_view(
        api_info,
        generator_class=schema_generator,
        public=True,
        permission_classes=(permissions.AllowAny,),
        patterns=api_url_patterns,
    ).without_ui(cache_timeout=get_docs_cache_timeout())


def make_docs_ui_view(api_info, api_url_patterns=None):
    """
    Build View for browsable API documentation.

    Arguments:
        api_info (openapi.Info): Information about the API.
        api_url_patterns (list of url patterns): URL patterns that API docs will be generated for

    Returns: View

    Example::

        from edx_api_doc_tools import make_api_info, make_docs_ui_view
        api_info = make_api_info(title="Awesome API", version="v42")
        my_ui_view = make_docs_ui_view(api_info)
    """
    schema_generator = get_schema_generator(api_url_patterns)

    return get_schema_view(
        api_info,
        generator_class=schema_generator,
        public=True,
        permission_classes=(permissions.AllowAny,),
        patterns=api_url_patterns,
    ).with_ui('swagger', cache_timeout=get_docs_cache_timeout())


class ApiSchemaGenerator(OpenAPISchemaGenerator):
    """
    A schema generator for ``/api/*``.

    Only includes endpoints in the ``/api/*`` url tree, and sets the path prefix
    appropriately.
    """

    def get_endpoints(self, request):
        """
        Return dict of endpoints to be displayed.
        """
        endpoints = super().get_endpoints(request)
        subpoints = {p: v for p, v in endpoints.items() if p.startswith("/api/")}
        return subpoints

    def determine_path_prefix(self, paths):
        """
        Return common prefix for all paths.
        """
        return "/api/"


def get_schema_generator(patterns):
    """
    Get correct schema generator.

    Defaults to ApiSchemaGenerator if no url patterns are specified, meaning
    that base path will be "/api".

    Arguments:
        patterns (list of url patterns): URL patterns that API docs will be generated for

    Returns:
        Schema generator object.
    """
    if patterns:
        return OpenAPISchemaGenerator
    else:
        return ApiSchemaGenerator


def get_docs_cache_timeout():
    """
    Return OPENAPI_CACHE_TIMEOUT setting, or zero if it's not defined.
    """
    try:
        return settings.OPENAPI_CACHE_TIMEOUT
    except AttributeError:
        return 0
