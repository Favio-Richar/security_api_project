from rest_framework import serializers

class DNSRecordSerializer(serializers.Serializer):
    A = serializers.ListField(child=serializers.CharField(), required=False)
    AAAA = serializers.ListField(child=serializers.CharField(), required=False)
    CNAME = serializers.ListField(child=serializers.CharField(), required=False)
    MX = serializers.ListField(child=serializers.CharField(), required=False)
    NS = serializers.ListField(child=serializers.CharField(), required=False)
    SOA = serializers.ListField(child=serializers.CharField(), required=False)
    TXT = serializers.ListField(child=serializers.CharField(), required=False)

class WhoisSerializer(serializers.Serializer):
    registrar = serializers.CharField(allow_null=True, required=False)
    creation_date = serializers.CharField(allow_null=True, required=False)
    expiration_date = serializers.CharField(allow_null=True, required=False)
    name_servers = serializers.ListField(child=serializers.CharField(), required=False)
    status = serializers.ListField(child=serializers.CharField(), required=False)
    emails = serializers.ListField(child=serializers.CharField(), required=False)
    country = serializers.CharField(allow_null=True, required=False)
    whois_server = serializers.CharField(allow_null=True, required=False)
    updated_date = serializers.CharField(allow_null=True, required=False)
    domain_name = serializers.CharField(allow_null=True, required=False)

class NmapPortSerializer(serializers.Serializer):
    port = serializers.CharField()
    protocol = serializers.CharField()
    state = serializers.CharField()
    service = serializers.DictField()

class NmapHostSerializer(serializers.Serializer):
    ip = serializers.CharField()
    ports = NmapPortSerializer(many=True)

class DNSReportSerializer(serializers.Serializer):
    domain = serializers.CharField()
    resolved_at = serializers.CharField()
    records = DNSRecordSerializer()
    whois = WhoisSerializer()
    nmap = NmapHostSerializer(many=True)
