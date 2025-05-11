from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import threading

from core.infrastructure.scanners.google_dorks import perform_dorks
from core.infrastructure.scanners.nmap_scan import perform_nmap_scan
from core.infrastructure.scanners.whois_scan import perform_whois_scan
from core.infrastructure.scanners.dns_scan import DNSResolver


class DNSScanView(APIView):
    def post(self, request):
        domain = request.data.get('domain')
        if not domain:
            return Response({'error': 'El parámetro "domain" es obligatorio.'}, status=400)

        resolver = DNSResolver(domain)

        # Parte DNS: siempre debe ejecutarse
        try:
            resolver.resolve_all()
        except:
            resolver.report["records"] = {"error": "Error al resolver DNS"}

        # Parte WHOIS: si falla, ignora
        try:
            resolver.resolve_whois()
        except:
            resolver.report["whois"] = {"error": "Error en WHOIS"}

        # Parte Nmap: si falla, ignora
        try:
            resolver.scan_with_nmap()
        except:
            resolver.report["nmap"] = [{"error": "Error en escaneo Nmap"}]

        return Response(resolver.report, status=200)


class GoogleDorksView(APIView):
    def post(self, request):
        query = request.data.get('query')
        if not query:
            return Response({'error': 'El parámetro "query" es obligatorio.'}, status=400)

        try:
            results = perform_dorks(query)
            return Response(results, status=200)
        except:
            return Response([], status=200)


class NmapScanView(APIView):
    def post(self, request):
        ip = request.data.get('ip')
        if not ip:
            return Response({'error': 'El parámetro "ip" es obligatorio.'}, status=400)

        try:
            result = perform_nmap_scan(ip)
            return Response(result, status=200)
        except:
            return Response({'error': 'Fallo el escaneo Nmap'}, status=200)


class WhoisScanView(APIView):
    def post(self, request):
        domain = request.data.get('domain')
        if not domain:
            return Response({'error': 'El parámetro "domain" es obligatorio.'}, status=400)

        try:
            result = perform_whois_scan(domain)
            return Response(result, status=200)
        except:
            return Response({'error': 'Fallo WHOIS'}, status=200)
