# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.infrastructure.adapters.scanner_adapter import get_dns_report, search_google_dorks
from .serializers import DNSReportSerializer, GoogleDorkResultSerializer
import threading

class DNSScanView(APIView):
    def post(self, request):
        domain = request.data.get('domain')
        if not domain:
            return Response({'error': 'El parámetro "domain" es obligatorio.'}, status=400)

        try:
            result_container = {}

            def run_report():
                result_container['report'] = get_dns_report(domain)

            t = threading.Thread(target=run_report)
            t.start()
            t.join(timeout=25)

            if 'report' not in result_container:
                return Response({'error': 'Tiempo de espera agotado'}, status=504)

            serializer = DNSReportSerializer(result_container['report'])
            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=500)


class GoogleDorksView(APIView):
    def post(self, request):
        query = request.data.get('query')
        if not query:
            return Response({'error': 'El parámetro "query" es obligatorio.'}, status=400)

        try:
            results = search_google_dorks(query)
            serializer = GoogleDorkResultSerializer(results, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
