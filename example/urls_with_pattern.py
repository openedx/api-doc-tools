"""
REST API URLs for testing make_docs_urls with url pattern specified.
"""

from django.conf.urls import url

from edx_api_doc_tools import make_api_info, make_docs_urls

from .views import HedgehogInfoView, HedgehogUndocumentedView


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
