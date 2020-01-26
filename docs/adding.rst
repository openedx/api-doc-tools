.. _adding:

Adding edx-api-doc-tools to your project
========================================

First, add ``edx-api-doc-tools`` to your requirements and install it into your
environment.

Next, add the following to your list of installed apps in Django settings::

    INSTALLED_APPS = (
        ... # your other installed apps
        drf_yasg,
        edx_api_doc_tools,
    )

Then, in ``urls.py``::

    ...
    from edx_api_doc_tools import make_api_info, make_docs_urls
    ...
    api_info = make_api_info(title="Registrar API", version="v2")
    urlpatterns += make_docs_urls(api_info)


Your should now be able to load the Swagger UI in a browser at
`https://${your_service}/api-docs`.  Note that by default, documentation is
only generated for views under the root path ``/api``.  Generation for other
views is possible but requires some extra configuration.

Finally, you can enrich the generated documentation::

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

