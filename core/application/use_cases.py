from core.domain.entities import DNSReport
from core.infrastructure.scanners.dns_scan import DNSResolver
from datetime import datetime

def generate_dns_report(domain: str) -> DNSReport:
    scanner = DNSResolver(domain)
    scanner.resolve_all()
    scanner.resolve_whois()
    scanner.scan_with_nmap()

    return DNSReport(
        domain=domain,
        resolved_at=scanner.report["resolved_at"],
        records=scanner.report["records"],
        whois=scanner.report["whois"],
        nmap=scanner.report["nmap"]
    )
