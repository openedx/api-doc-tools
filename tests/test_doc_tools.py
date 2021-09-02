"""
Tests for API docs tooling.
"""

import json
import os.path
from unittest.mock import patch

import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase
from django.test.utils import override_settings

from edx_api_doc_tools.apps import EdxApiDocToolsConfig
from edx_api_doc_tools.internal_utils import split_docstring
from example import urls as example_urls
from example import urls_with_pattern as test_pattern_urls


@override_settings(ROOT_URLCONF=example_urls.__name__)
class DocViewTests(SimpleTestCase):
    """
    Test that the API docs generated from the example Hedgehog API look right.
    """
    maxDiff = None  # Always show full diff output.

    base_path = os.path.dirname(__file__)
    path_of_expected_schema = os.path.join(base_path, 'expected_schema.json')
    path_of_actual_schema = os.path.join(base_path, 'actual_schema.json')

    def test_get_data_view(self):
        """
        Test that the generated API schema equals the reference schema.

        How this test works:
        * Generate a Swagger schema by GETting /swagger.json, and then dumping it to
          actual_schema.json.
        * Load example_schema.json.
        * Assert that actual_schema.json and example_schema.json are equivalent.

        If you make a change to the doc tools or the example API that change the
        generated schema, here's how to update this test:
        * Run the test, which should fail with an AssertionError about the
          generated schema.
        * Copy the contents of actual_schema.json into https://editor.swagger.io
        * Make sure the browsable API looks correct,
          and make sure the contents of the schema file look sane.
        * If everything looks right, copy actual_schema.json into expected_schema.json
          and commit the change, making it the new reference schema.
        """
        response = self.client.get('/swagger.json')
        assert response.status_code == 200
        actual_schema = response.json()
        with open(self.path_of_actual_schema, 'w',  encoding='utf-8') as f:
            json.dump(actual_schema, f, indent=4, sort_keys=True)
        with open(self.path_of_expected_schema,  encoding='utf-8') as schema_file:
            expected_schema = json.load(schema_file)
        assert actual_schema == expected_schema, (
            "Generated schema (dumped to {}) "
            "did not match schema loaded from expected_schema.json."
            .format(os.path.relpath(self.path_of_actual_schema))
        )

    def test_get_ui_view(self):
        """
        Test that the UI view returns a page with the expected title.

        We can't assert anything about page content, because that is all loaded
        via an AJAX call to /api-docs/?format=openapi
        """
        response = self.client.get('/api-docs/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert '<title>edX Hedgehog Service API</title>' in content

    def test_ui_data_endpoint(self):
        """
        Test that the the endpoint that the UI calls via AJAX returns the same data
        as the schema endpoint.
        """
        data_response = self.client.get('/swagger.json', )
        ui_data_response = self.client.get('/api-docs/?format=openapi')
        assert ui_data_response.status_code == data_response.status_code == 200
        expected = data_response.json()
        # Cannot use `.json()` because response has content type
        # 'application/openapi+json'.
        actual = json.loads(ui_data_response.content.decode('utf-8'))
        assert actual == expected


@pytest.mark.parametrize("docstring, summary, description", [
    (None, None, None),
    ("", None, None),
    ("hello", "hello", None),
    (
        """
        A summary.
        """,
        "A summary.",
        None,
    ),
    (
        """
        This is an awesome function.

        It does lots
        of cool things.

        Really, lots.
        """,
        "This is an awesome function.",
        "It does lots\nof cool things.\n\nReally, lots."
    ),
])
def test_split_docstring(docstring, summary, description):
    actual_summary, actual_description = split_docstring(docstring)
    assert actual_summary == summary
    assert actual_description == description


class AppConfigTests(SimpleTestCase):
    """
    Tests for EdxApiDocToolsConfig.
    """
    original_app_ready_fn = EdxApiDocToolsConfig.ready

    def setUp(self):
        super().setUp()
        self.called_app_ready = False

    def test_app_ready_fails_without_yasg(self):
        """
        Assert that `EdxApiDocToolsConfig.ready` requires 'drf_yasg' to be installed.
        """
        installed_apps_sans_yasg = [
            app_label for app_label in settings.INSTALLED_APPS
            if app_label != 'drf_yasg'
        ]
        with patch.object(EdxApiDocToolsConfig, 'ready', new=self.mock_app_ready):
            with override_settings(INSTALLED_APPS=installed_apps_sans_yasg):
                # `override_settings` causes Django to reload,
                # which should trigger a call to `mock_app_ready`.
                pass
        assert self.called_app_ready

    def mock_app_ready(self, *args, **kwargs):
        """
        Wrap EdxApiDocToolsConfig.ready.

        Assert that it complain that drf_yasg isn't installed.
        """
        with pytest.raises(ImproperlyConfigured, match="drf_yasg\' must also be added"):
            self.original_app_ready_fn(*args, **kwargs)
        self.called_app_ready = True


@override_settings(ROOT_URLCONF=test_pattern_urls.__name__)
class DocViewPatternTests(SimpleTestCase):
    """
    Test that the API docs generated from the example Hedgehog API look right.
    """
    maxDiff = None  # Always show full diff output.

    base_path = os.path.dirname(__file__)
    path_of_expected_schema = os.path.join(base_path, 'expected_schema_with_patterns.json')
    path_of_actual_schema = os.path.join(base_path, 'actual_schema_with_patterns.json')

    def test_get_data_view(self):
        """
        Same test as above, but with different urls and expected_schema
        """
        response = self.client.get('/swagger.json')
        assert response.status_code == 200
        actual_schema = response.json()
        with open(self.path_of_actual_schema, 'w',  encoding='utf-8') as f:
            json.dump(actual_schema, f, indent=4, sort_keys=True)
        with open(self.path_of_expected_schema,  encoding='utf-8') as schema_file:
            expected_schema = json.load(schema_file)
        assert actual_schema == expected_schema, (
            "Generated schema (dumped to {}) "
            "did not match schema loaded from expected_schema_with_patterns.json."
            .format(os.path.relpath(self.path_of_actual_schema))
        )
