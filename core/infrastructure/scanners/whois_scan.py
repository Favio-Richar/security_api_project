import whois
import json
from datetime import datetime
from pathlib import Path
import os

def perform_whois_scan(domain):
    try:
        data = whois.whois(domain)
        result = {
            "domain": domain,
            "scanned_at": datetime.utcnow().isoformat(),
            "registrar": data.registrar,
            "creation_date": str(data.creation_date),
            "expiration_date": str(data.expiration_date),
            "name_servers": data.name_servers,
            "status": data.status,
            "emails": data.emails,
            "country": data.country,
            "whois_server": data.whois_server,
            "updated_date": str(data.updated_date),
            "domain_name": data.domain_name,
        }
    except Exception as e:
        result = {"error": str(e)}

    Path("DATA-REPORT-WHOIS").mkdir(exist_ok=True)
    output_file = f"DATA-REPORT-WHOIS/{domain.replace('.', '_')}_whois_report.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
    print(f"✅ WHOIS report saved to: {output_file}")
    return result

# Ejemplo de uso
if __name__ == "__main__":
    domain = "educativaipchile.cl"
    perform_whois_scan(domain)
