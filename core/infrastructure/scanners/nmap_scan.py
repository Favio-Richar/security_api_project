import subprocess
import xml.etree.ElementTree as ET
import json
from pathlib import Path
from datetime import datetime
import os

def perform_nmap_scan(ip):
    xml_file = f"/tmp/nmap_scan_{ip}.xml"
    try:
        subprocess.run(
            ["nmap", "-A", "-Pn", "-T4", "-oX", xml_file, ip],
            check=True,
            capture_output=True
        )
    except subprocess.CalledProcessError as e:
        return {"error": f"Nmap failed: {str(e)}"}

    result = {
        "ip": ip,
        "scanned_at": datetime.utcnow().isoformat(),
        "ports": []
    }

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        ports = root.find("host").find("ports")
        if ports is not None:
            for port in ports.findall("port"):
                port_info = {
                    "port": port.attrib["portid"],
                    "protocol": port.attrib["protocol"],
                    "state": port.find("state").attrib.get("state", ""),
                    "service": {}
                }
                service = port.find("service")
                if service is not None:
                    port_info["service"] = {
                        "name": service.attrib.get("name", ""),
                        "product": service.attrib.get("product", ""),
                        "version": service.attrib.get("version", "")
                    }
                result["ports"].append(port_info)
    except Exception as e:
        result["error"] = str(e)
    finally:
        if os.path.exists(xml_file):
            os.remove(xml_file)

    Path("DATA-REPORT-NMAP").mkdir(exist_ok=True)
    output_file = f"DATA-REPORT-NMAP/{ip.replace('.', '_')}_nmap_report.json"
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)
    print(f"✅ Nmap report saved to: {output_file}")
    return result

# Ejemplo de uso
if __name__ == "__main__":
    perform_nmap_scan("8.8.8.8")
