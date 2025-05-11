from core.application.use_cases import generate_dns_report
from core.infrastructure.scanners.google_dorks import perform_dorks

# Función que se llama desde la vista DNSScanView
def get_dns_report(domain: str) -> dict:
    report = generate_dns_report(domain)
    return {
        "domain": report.domain,
        "resolved_at": report.resolved_at,
        "records": report.records,
        "whois": report.whois,
        "nmap": report.nmap
    }

# Función que se llama desde la vista GoogleDorksView
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
