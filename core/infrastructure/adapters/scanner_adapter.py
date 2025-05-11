from core.application.use_cases import generate_dns_report
from core.infrastructure.scanners.google_dorks import perform_dorks
from core.infrastructure.scanners.nmap_scan import perform_nmap_scan
from core.infrastructure.scanners.whois_scan import perform_whois_scan

# DNS
def get_dns_report(domain: str) -> dict:
    report = generate_dns_report(domain)
    return {
        "domain": report.domain,
        "resolved_at": report.resolved_at,
        "records": report.records,
        "whois": report.whois,
        "nmap": report.nmap
    }

# Google Dorks
def search_google_dorks(query: str) -> list:
    results = perform_dorks(query)
    return [
        {
            "title": r.get("title", ""),
            "link": r.get("link", ""),
            "snippet": r.get("snippet", "")
        }
        for r in results
    ]

# Nmap
def scan_nmap(ip: str) -> dict:
    return perform_nmap_scan(ip)

# WHOIS
def scan_whois(domain: str) -> dict:
    return perform_whois_scan(domain)
