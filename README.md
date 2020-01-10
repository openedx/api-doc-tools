# edX API Documentation Tools

<p align="center">
    <a href="https://pypi.python.org/pypi/api-doc-tools/" alt="PyPI">
        <img src="https://img.shields.io/pypi/v/api-doc-tools.svg" />
    </a>
    <a href="https://travis-ci.org/edx/api-doc-tools" alt="Travis">
        <img src="https://travis-ci.org/edx/api-doc-tools.svg?branch=master" />
    </a>
    <a href="http://codecov.io/github/edx/api-doc-tools?branch=master" alt="Codecov">
        <img src="http://codecov.io/github/edx/api-doc-tools/coverage.svg?branch=master" />
    </a>
    <a href="http://api-doc-tools.readthedocs.io/en/latest/" alt="Documentation">
        <img src="https://readthedocs.org/projects/api-doc-tools/badge/?version=latest" />
    </a>
    <a href="https://pypi.python.org/pypi/api-doc-tools/" alt="Supported >
        <img ython versions" src="https://img.shields.io/pypi/pyversions/api-doc-tools.svg" />
    </a>
    <a href="https://github.com/edx/api-doc-tools/blob/master/LICENSE.txt" alt="License">
        <img src="https://img.shields.io/github/license/edx/api-doc-tools.svg" />
    </a>
</p>

A toolkit for documenting REST APIs that are created with [DRF](https://www.django-rest-framework.org/).

The tools use [drf-yasg](https://github.com/axnsan12/drf-yasg)
(DRF, yet another Swagger generator)
to generate an [OpenAPI Specification](https://swagger.io/docs/specification/about/),
which is a .json/.yaml file that describes your API.
Additionally, this package makes it easy to configure your service
to expose generated OpenAPI specification under `/api-docs.yaml`
and to serve interactive documentation under `/api-docs`.

This library is intended for use with [Open edX](https://open.edx.org/) services,
but could be used to document any Django REST Framework API.

## Quick Start

First, add ``edx-api-doc-tools`` to your requirements
and install it into your environment.

Next, add the following to your list of installed apps in Django settings:
```python
    INSTALLED_APPS = (
        ... # your other installed apps
        drf_yasg,
        edx_api_doc_tools,
    )
```

Then, in ``urls.py``:
```python
...
from edx_api_doc_tools import make_api_info, make_docs_urls
...
api_info = make_api_info(title="Registrar API", version="v2")
urlpatterns += make_docs_urls(api_info)
```

Your should now be able to load the Swagger UI in a browser at
https://${your_service}/api-docs.
Note that by default,
documentation is only generated for views under the root path ``/api``.
Generation for other views is possible but requires some extra configuration.

Finally, you can enrich the generated documentation:
```python
...
from edx_api_doc_tools import parameter, schema
...
class MyView(APIView):

    @schema(
        parameters=[
            parameter('min_date', str, 'Filter response by minimum date.'),
        ],
        responses={
            403: 'User lacks required permission.'
            404: 'Resource does not exist.'
            # Note that 2xx response is automatically figured out by drf-yasg,
            # with reponse schema coming from the serializer, if declared.
        },
    )
    def get(self, request):
        """
        Get the resource.

        This docstring will be used in the OpenAPI spec, and *supports Markdown!*
        """
        ...
```

# Documentation

Comphrehensive documentation is coming soon.
For now, check out the `example/` directory,
which shows an fake API using these tools to generate documentation.

# License

The code in this repository is licensed under the Apache Software License 2.0 unless
otherwise noted.

Please see `LICENSE.txt` for details.

# How To Contribute

Contributions are very welcome.

Please read [How To Contribute](https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst>)
for details.

Even though they were written with `edx-platform` in mind, the guidelines
should be followed for Open edX code in general.

The pull request description template should be automatically applied if you are creating a pull request from GitHub. Otherwise you
can find it at [PULL_REQUEST_TEMPLATE.md](https://github.com/edx/api-doc-tools/blob/master/.github/PULL_REQUEST_TEMPLATE.md).

The issue report template should be automatically applied if you are creating an issue on GitHub as well. Otherwise you
can find it at [ISSUE_TEMPLATE.md](https://github.com/edx/api-doc-tools/blob/master/.github/ISSUE_TEMPLATE.md>).

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Getting Help
------------

Have a question about this repository, or about Open edX in general?  Please
refer to this [list of resources](https://open.edx.org/getting-help)
if you need any assistance.


