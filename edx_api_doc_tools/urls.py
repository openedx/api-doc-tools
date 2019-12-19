# -*- coding: utf-8 -*-
"""
URLs for edx_api_doc_tools.
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'', TemplateView.as_view(template_name="edx_api_doc_tools/base.html")),
]
