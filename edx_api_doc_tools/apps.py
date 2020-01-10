"""
App for documenting REST APIs, generating spec files, and serving specs as a UI.

Under the hood, this app uses drf-yasg
("Yet Another Swagger Generator for DRF")
to generate API spec. It then uses Swagger to serve that spec.
"""

from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig, apps
from django.core.exceptions import ImproperlyConfigured


class EdxApiDocToolsConfig(AppConfig):
    """
    Configuration for this app.

    Note that 'drf_yasg' must be added to INSTALLED_APPS as well.
    """
    name = 'edx_api_doc_tools'
    verbose_name = 'edX REST API Documentation Tools'

    def ready(self):
        """
        Check whether 'drf_yasg' is in INSTALLED_APPS.

        We prefer to throw an error upon initialization, because otherwise,
        a developer won't know something is wrong until they try to render the
        docs UI, at which point they'll just see a template load error.

        Overrides `AppConfig.ready`.
        """
        for app in apps.get_app_configs():
            if app.label == 'drf_yasg':
                return
        raise ImproperlyConfigured(
            "To use edx_api_doc_tools, "
            "'drf_yasg' must also be added to 'INSTALLED_APPS'."
        )
