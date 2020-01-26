.. _writing:

Writing API documentation
=========================

Documentation for API endpoints starts in the Python files, using docstrings
and decorators.


For an APIView
--------------

In an APIView, document your endpoints by adding the :func:`.schema` decorator
to your handler methods (get, post, etc).  The docstring of the method will
be used as the documentation.  The first line is the summary, and the rest of
the docstring is the description.  Everything is in Markdown format.

Additional arguments to the :func:`.schema` decorator provide details of the
parameters and responses.

For example::

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


For a ViewSet
-------------

In a ViewSet, you don't write explicit get, post, list, or retrieve methods, so
there aren't explicit docstrings to use for documentation.

In this case, you use the :func:`.schema_for` decorator on the class.  Its
first argument is the method name it applies to, and the second argument is
a docstring to use for that method.  The rest of the arguments are the same
as for :func:`.schema`.  You can use as many :func:`.schema_for` decorators
on a class as you need::

    @schema_for(
        "list",
        """
        Fetch the list of edX hedgehogs.

        Hedgehogs can be filtered by minimum weight (grams or ounces),
        their favorite food, whether they graduated college,
        or any combination of those criterion.
        """,
        parameters=[
            query_parameter('min-grams', int, "Filter on whether minimum weight (grams)."),
            query_parameter('min-ounces', float, "Filter hogs by minimum weight (ounces)."),
        ],
        responses={
            404: 'Hedgehog with given key not found.',
        },
    )
    @schema_for(
        "retrieve",
        """
        Fetch details for a _single_ hedgehog by key.
        """,
        parameters=[
            path_parameter(
                'hedgehog_key', str, "Key identifying the hog. Lowercase letters only."
            ),
        ],
        responses={
            404: 'Hedgehog with given key not found.',
        },
    )
    class HedgehogViewSet(ModelViewSet):
        ...



