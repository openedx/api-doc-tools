edX API Documentation Tools
===========================

|pypi| |CI| |codecov| |readthedocs| |pyversions| |license|

A toolkit for documenting REST APIs that are created with `DRF`_.

.. _DRF: https://www.django-rest-framework.org/

The tools use `drf-yasg`_ (DRF, yet another Swagger generator) to generate an
`OpenAPI Specification`_, which is a .json/.yaml file that describes your API.
Additionally, this package makes it easy to configure your service to expose
generated OpenAPI specification under `/api-docs.yaml` and to serve interactive
documentation under `/api-docs`.

.. _drf-yasg: https://github.com/axnsan12/drf-yasg
.. _OpenAPI Specification: https://swagger.io/docs/specification/about/

This library was developed for use with `Open edX`_ services, but could be used
to document any Django REST Framework API.

.. _Open edX: https://open.edx.org/


Quick Start
-----------

To start using this tool in your project, see
`Adding edx-api-doc-tools to your project <docs/adding.rst>`_.

To write docs using this tool, see
`Writing API documentation <docs/writing.rst>`_.


Documentation
-------------

Comphrehensive documentation is coming soon.  For now, check out the `example/`
directory, which shows a fake API using these tools to generate documentation.

License
-------

The code in this repository is licensed under the Apache Software License 2.0
unless otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

Contributions are very welcome.  Please read `How To Contribute`__ for details.
Even though they were written with `edx-platform` in mind, the guidelines
should be followed for all Open edX projects.

__ https://github.com/edx/edx-platform/blob/master/CONTRIBUTING.rst

The pull request description template should be automatically applied if you
are creating a pull request from GitHub. Otherwise you can find it at
`PULL_REQUEST_TEMPLATE.md`_.

The issue report template should be automatically applied if you are creating
an issue on GitHub as well. Otherwise you can find it at `ISSUE_TEMPLATE.md`_.

.. _PULL_REQUEST_TEMPLATE.md: .github/PULL_REQUEST_TEMPLATE.md
.. _ISSUE_TEMPLATE.md: .github/ISSUE_TEMPLATE.md

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email security@edx.org.

Getting Help
------------

Have a question about this repository, or about the Open edX project in general?  Please refer to this `list of resources <https://open.edx.org/getting-help>`_ if you need any assistance.



.. |pypi| image:: https://img.shields.io/pypi/v/edx-api-doc-tools.svg
    :target: https://pypi.python.org/pypi/edx-api-doc-tools/
    :alt: PyPI
.. |CI| image:: https://github.com/edx/api-doc-tools/workflows/Python%20CI/badge.svg?branch=master
    :target: https://github.com/edx/api-doc-tools/actions?query=workflow%3A%22Python+CI%22
    :alt: CI
.. |codecov| image:: http://codecov.io/github/edx/api-doc-tools/coverage.svg?branch=master
    :target: http://codecov.io/github/edx/api-doc-tools?branch=master
    :alt: Codecov
.. |readthedocs| image:: https://readthedocs.org/projects/edx-api-doc-tools/badge/?version=latest
    :target: http://edx-api-doc-tools.readthedocs.io/en/latest/
    :alt: Documentation
.. |pyversions| image:: https://img.shields.io/pypi/pyversions/edx-api-doc-tools.svg
    :target: https://pypi.python.org/pypi/edx-api-doc-tools/
    :alt: Supported
.. |license| image:: https://img.shields.io/github/license/edx/api-doc-tools.svg
    :target: https://github.com/edx/api-doc-tools/blob/master/LICENSE.txt
    :alt: License
