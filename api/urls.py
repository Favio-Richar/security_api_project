from django.urls import path
from .views import (
    DNSScanView,
    GoogleDorksView,
    NmapScanView,
    WhoisScanView
)

urlpatterns = [
    path('scan/dns/', DNSScanView.as_view(), name='scan-dns'),
    path('scan/google/', GoogleDorksView.as_view(), name='scan-google'),
    path('scan/nmap/', NmapScanView.as_view(), name='scan-nmap'),
    path('scan/whois/', WhoisScanView.as_view(), name='scan-whois'),
]
