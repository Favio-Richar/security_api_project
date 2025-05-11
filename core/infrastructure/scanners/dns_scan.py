import json
import dns.resolver
import whois
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import os

class DNSResolver:
    def __init__(self, domain, record_types=None):
        self.domain = domain
        self.record_types = record_types or ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = ["8.8.8.8", "1.1.1.1"]  # ⚠️ Usar DNS externos
        self.report = {
            "domain": domain,
            "resolved_at": datetime.utcnow().isoformat(),
            "records": {},
            "whois": {},
            "nmap": []
        }

    def resolve_all(self):
        for record_type in self.record_types:
            try:
                answers = self.resolver.resolve(self.domain, record_type, lifetime=5)
                self.report["records"][record_type] = [str(data) for data in answers]
            except Exception:
                self.report["records"][record_type] = []

    def resolve_whois(self):
        try:
            w = whois.whois(self.domain)
            self.report["whois"] = {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "name_servers": w.name_servers,
                "status": w.status,
                "emails": w.emails,
                "country": w.country,
                "whois_server": w.whois_server,
                "updated_date": str(w.updated_date),
                "domain_name": w.domain_name,
            }
        except Exception as e:
            self.report["whois"] = {"error": str(e)}

    def extract_ips_for_scan(self):
        ips = self.report["records"].get("A", [])
        ns_records = self.report["records"].get("NS", [])
        for ns in ns_records:
            try:
                ns_ip = self.resolver.resolve(ns.rstrip('.'), 'A')
                ips.extend([str(ip) for ip in ns_ip])
            except:
                continue
        return list(set(ips))

    def scan_with_nmap(self):
        print(f"🛠️ Ejecutando Nmap para: {self.domain}")
        try:
            ips = self.extract_ips_for_scan()
            print(f"🧠 IPs encontradas: {ips}")
            for ip in ips:
                try:
                    xml_output = f"/tmp/nmap_{ip}.xml"
                    print(f"⏳ Escaneando {ip}...")
                    subprocess.run(
                        ["nmap", "-F", "-T4", "-Pn", "-oX", xml_output, ip],
                        check=True,
                        capture_output=True,
                        timeout=10  # ⏱️ Máximo 10 segundos por IP
                    )
                    self.parse_nmap(xml_output)
                    os.remove(xml_output)
                    print(f"✅ Escaneo de {ip} completado")
                except subprocess.TimeoutExpired:
                    print(f"⏱️ Nmap TIMEOUT en {ip}")
                except subprocess.CalledProcessError as e:
                    print(f"⚠️ Error al ejecutar Nmap en {ip}: {e}")
        except Exception as e:
            print(f"❌ Error general en escaneo con Nmap: {e}")
        finally:
            self.export_to_json()

    def parse_nmap(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        host = root.find("host")

        host_info = {"ip": "", "ports": []}
        address = host.find("address")
        if address is not None:
            host_info["ip"] = address.attrib["addr"]

        ports = host.find("ports")
        if ports is not None:
            for port in ports.findall("port"):
                port_info = {
                    "port": port.attrib["portid"],
                    "protocol": port.attrib["protocol"],
                    "state": port.find("state").attrib["state"],
                    "service": {}
                }
                service = port.find("service")
                if service is not None:
                    port_info["service"] = {
                        "name": service.attrib.get("name", ""),
                        "product": service.attrib.get("product", ""),
                        "version": service.attrib.get("version", "")
                    }
                host_info["ports"].append(port_info)

        self.report["nmap"].append(host_info)

    def export_to_json(self):
        output_path = f"DATA-REPORT-DNS/{self.domain.replace('.', '_')}_dns_report.json"
        Path("DATA-REPORT-DNS").mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=4, default=str)
        print(f"✅ Reporte guardado en: {output_path}")
