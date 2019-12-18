"""
Data definitions for API schemas.

Mostly, we just use the definitions in drf_yasg.openapi
"""
from __future__ import absolute_import, unicode_literals

from drf_yasg import openapi


# Python 3 doesn't have a builtin `file` type,
# so we need a constant instead.
FILE_PARAM = 'file'


# A map from builtin Python types to the corresponding OpenAPI type string constant.
# The built-in types can be passed to the `parameter` function  in place of the
# OpenAPI strings for convenience.
_PARAM_TYPE_MAP = {
    object: openapi.TYPE_OBJECT,
    str: openapi.TYPE_STRING,
    float: openapi.TYPE_NUMBER,
    int: openapi.TYPE_INTEGER,
    bool: openapi.TYPE_BOOLEAN,
    list: openapi.TYPE_ARRAY,
    FILE_PARAM: openapi.TYPE_FILE,
}


PARAM_TYPES = frozenset(_PARAM_TYPE_MAP.keys())


def path_parameter(name, param_type, description=None):
    """
    Define a parameter in the endpoint's path.

    Type must still be specified.
    """
    return parameter(name, ParameterLocation.PATH, param_type, description=description)


def query_parameter(name, param_type, description=None):
    """
    Define a parameter in the endpoint's querystring.

    Type must still be specified.
    """
    return parameter(name, ParameterLocation.QUERY, param_type, description=description)


def string_parameter(name, in_, description=None):
    """
    Define a string parameter.

    Location must still be specified.
    """
    return parameter(name, in_, str, description=description)


def parameter(name, in_, param_type, description=None):
    """
    Define a typed parameter.

    Arguments:
        name (str): The name of the parameter.
        in_ (ParameterLocation attribute): How the parameter is passed in.
        param_type (type|str): a member of `PARAM_TYPES`.
        description (str): Description of the parameter.

    Returns: openapi.Parameter
    """
    try:
        openapi_type = _PARAM_TYPE_MAP[param_type]
    except KeyError:
        raise ValueError(
            'param_type must be a member of the set {}'.format(PARAM_TYPES)
        )
    return openapi.Parameter(
        name,
        in_,
        type=openapi_type,
        description=description,
    )


class ParameterLocation:
    """
    Location of API parameter in request.
    """
    BODY = openapi.IN_BODY
    PATH = openapi.IN_PATH
    QUERY = openapi.IN_QUERY
    FORM = openapi.IN_FORM
    HEADER = openapi.IN_HEADER
    __ALL__ = {BODY, PATH, QUERY, FORM, HEADER}
