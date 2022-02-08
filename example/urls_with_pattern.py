"""
REST API URLs for testing make_docs_urls with url pattern specified.
"""

from django.urls import path

from edx_api_doc_tools import make_api_info, make_docs_urls

from .views import HedgehogInfoView, HedgehogUndocumentedView


urlpatterns = []

urlpatterns += [
    path('/api/hedgehog/v1/info', HedgehogInfoView.as_view()),
    path('/api/hedgehog/v1/undoc-view', HedgehogUndocumentedView.as_view()),
    path('/test/hedgehog/v1/info', HedgehogInfoView.as_view()),
    path('/test/hedgehog/v1/undoc-view', HedgehogUndocumentedView.as_view()),
]

display_urls = [
    path('/test/hedgehog/v1/info', HedgehogInfoView.as_view()),
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
