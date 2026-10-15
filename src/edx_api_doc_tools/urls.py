"""
URLs for edx_api_doc_tools.
"""
from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name="edx_api_doc_tools/base.html")),
]
