"""
App for documenting REST APIs, generating spec files, and serving specs as a UI.

Under the hood, this app uses drf-yasg
("Yet Another Swagger Generator for DRF")
to generate API spec. It then uses Swagger to serve that spec.
"""

from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class EdxApiDocToolsConfig(AppConfig):
    """
    Configuration for this app.

    # TODO: How do we make it so 'drf_yasg' is automatically
    # installed as a Django app when 'edx_api_doc_tools'
    # is added to INSTALLED_APPS? Currently, both must be added manually.
    """
    name = 'edx_api_doc_tools'
    verbose_name = 'edX REST API Documentation Tools'
