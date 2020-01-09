"""
Utility functions internal to this package.
"""
from __future__ import absolute_import, unicode_literals

import textwrap


def dedent(text):
    """
    Dedent multi-line text nicely.

    An initial empty line is ignored so that triple-quoted strings don't need
    to start with a backslash.
    """
    if "\n" in text:
        first, rest = text.split("\n", 1)
        if not first.strip():
            # First line is blank, discard it.
            text = rest
    return textwrap.dedent(text)


def split_docstring(docstring):
    """
    Split a docstring into a summary and a description.

    Arguments:
        docstring (str): the docstring

    Returns:
        summary (str or None): a one-line summary.
        description (str or None): the multi-line description.
    """
    summary = None
    description = None
    if docstring:
        doc_lines = docstring.strip().split("\n")
        if doc_lines:
            summary = doc_lines[0].strip()
        if len(doc_lines) > 1:
            description = dedent("\n".join(doc_lines[1:]))
    return summary, description
