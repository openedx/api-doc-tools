.. _excluding:

Excluding API endpoints from documentation
==========================================

Once installed, ``edx-api-doc-tools`` will automatically generate browsable
documentation for all API endpoints within the ``/api/`` path.
This may not be what you want.

Analogous to the :func:`schema` and :func:`schema_for` decorators,
there exist the ``exclude_schema`` and :func:`exclude_schema_for` decorators,
both of which prevent the target endpoint from appearing in your API documentation.
The former is useful when your endpoint handler is defined directly in your source file,
whereas the latter is useful when the handler is implemented by a base class.

Furthermore, :func:`exclude_schema_for` can be used on a View or Viewset to
exclude multiple endpoints at once.
If you wish to exclude *all* endpoints for View or Viewset, decorate it with
``exclude_schema_for_all``.

For example::

    ...
    from edx_api_doc_tools import exclude_schema, exclude_schema_for, exclude_schema_for_all
    ...
    class MyViewsetWithSomeDocs(ViewSet):
        def retrieve(...):
            """
            This will appear in the docs.
            """

        @exclude_schema
        def update(...):
            """
            This will NOT appear in the docs.
            """


    @exclude_schema_for_all
    class MyViewsetWithNoDocs(ViewSet):
        def retrieve(...):
            """
            This will  NOT appear in the docs.
            """
        def update(...):
            """
            This will NOT appear in the docs.
            """


    # Note that ``ModelAPIView`` comes with pre-implemented handlers for
    # GET, POST, PUT, PATCH, and DESTROY.


    class MyModelViewWithAllDocs(ModelAPIView):
        """
        Will have docs for GET, POST, PUT, PATCH, and DESTROY.
        """

    @exclude_schema_for('destroy')
    class MyModelViewWithMostDocs(ModelAPIView):
        """
        Will have docs for GET, POST, PUT, and PATCH.
        """

    @exclude_schema_for('put', 'patch', 'destroy')
    class MyModelViewWithSomeDocs(ModelAPIView)
        """
        Will have docs for GET and POST.
        """

    @exclude_schema_for_all
    class MyViewModelViewNoDocs(ModelAPIView)
        """
        ModelAPIView has handlers for GET, POST, PUT, PATCH, and DESTROY,
        but we will not see any docs for this view.
        """

    @exclude_schema_for_all
    class MyViewWithMostDocs(APIView)
        def get(self, request):
            """
            This won't appear in the docs.
            """
        def post(self, request):
            """
            Nor will this.
            """

Additionally, api-docs can be generated only for specified URL patterns. This also
allows documentation for endpoints outside of the ``/api/`` path.

The following code will result in generated documentation only for the ``/test/hedgehog/v1/info`` endpoint::

    urlpatterns = []

    urlpatterns += [
        url(r'/api/hedgehog/v1/info', HedgehogInfoView.as_view()),
        url(r'/api/hedgehog/v1/undoc-view', HedgehogUndocumentedView.as_view()),
        url(r'/test/hedgehog/v1/info', HedgehogInfoView.as_view()),
        url(r'/test/hedgehog/v1/undoc-view', HedgehogUndocumentedView.as_view()),
    ]

    display_urls = [
        url(r'/test/hedgehog/v1/info', HedgehogInfoView.as_view()),
    ]

    urlpatterns += make_docs_urls(
        make_api_info(
            title="edX Hedgehog Service API",
            version="v1",
            email="hedgehog-support@example.com",
            description="A REST API for interacting with the edX hedgehog service.",
        ),
        api_url_patterns=display_urls,
    )
