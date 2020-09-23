"""
REST API URLs for reading and writing to the edX Hedgehog Database.
"""

from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from edx_api_doc_tools import make_api_info, make_docs_urls

from .views import HedgehogInfoView, HedgehogUndocumentedView, HedgehogUndocumentedViewset, HedgehogViewSet


urlpatterns = []

ROUTER = SimpleRouter()
ROUTER.register(
    r'api/hedgehog/v0/hogs', HedgehogViewSet, basename='hedgehog'
)
ROUTER.register(
    r'api/hedgehog/v0/undoc-viewset', HedgehogUndocumentedViewset, basename='undoc-viewset'
)
urlpatterns += ROUTER.urls

urlpatterns += [
    url(r'/api/hedgehog/v0/info', HedgehogInfoView.as_view()),
    url(r'/api/hedgehog/v0/undoc-view', HedgehogUndocumentedView.as_view()),
    url(r'/api/hedgehog/v1/info', HedgehogInfoView.as_view()),
    url(r'/api/hedgehog/v1/undoc-view', HedgehogUndocumentedView.as_view()),
]

urlpatterns += make_docs_urls(
    make_api_info(
        title="edX Hedgehog Service API",
        version="v0",
        email="hedgehog-support@example.com",
        description="A REST API for interacting with the edX hedgehog service.",
    ),
)
