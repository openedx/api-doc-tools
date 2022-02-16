Change Log
==========

..
   All enhancements and patches to edx_api_doc_tools will be documented
   in this file.  It adheres to the structure of http://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (http://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
----------

1.6.0 --- 2022-02-11
--------------------

* Dropped support for django 2.2, 3.0, 3.1
* Added support for Django 4.0

1.5.0 --- 2021-07-19
--------------------

* Added support for django 3.0, 3.1 and 3.2

1.4.3 --- 2021-07-15
--------------------

* Removed Django constraints from base.in

1.4.2 --- 2021-01-08
--------------------

* Dropped python3.5 support.

1.4.1 --- 2020-11-20
--------------------

* Updated the travis-badge in README.rst to point to travis-ci.com

1.4.0 --- 2020-10-05
--------------------

* Adding option to include a body parameter in requests.

1.3.2 --- 2020-09-23
--------------------

* Adding option to specify url patterns for generated docs.

1.3.1 --- 2020-05-29
--------------------

* Removing caniusepython3 as it is no longer needed since python3 upgrade.

1.3.0 --- 2020-04-30
--------------------

* Remove support for Django<2.2 and add support for python 3.8

1.2.0 --- 2020-03-20
--------------------

* Added three new decorators for excluding endpoints from API documentation generation:

  * ``@exclude_schema``
  * ``@exclude_schema_for(method_name)``
  * ``@exclude_all_schemas``


1.1.0 --- 2020-03-20
--------------------

* Compatibility with Django 2.1 and 2.2.


1.0.3 --- 2020-01-31
--------------------

* Added documentation.


1.0.2 --- 2020-01-17
--------------------

* First release on PyPI.
