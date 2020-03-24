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
