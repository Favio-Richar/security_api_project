class DNSReport:
    def __init__(self, domain, resolved_at, records, whois, nmap):
        self.domain = domain
        self.resolved_at = resolved_at
        self.records = records
        self.whois = whois
        self.nmap = nmap
