#!/usr/bin/env python3
"""
ZPHISHING APEX — Reconnaissance Module
Target reconnaissance and intelligence gathering
"""

import os
import json
import time
import socket
import whois
import dns.resolver
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
import shodan
import censys.search
import builtwith
import wappalyzer
import tldextract

@dataclass
class TargetInfo:
    domain: str
    ip: str
    nameservers: List[str]
    mx_records: List[str]
    technologies: List[str]
    subdomains: List[str]
    emails: List[str]

class ReconnaissanceModule:
    def __init__(self):
        self.shodan_client = shodan.Shodan(os.environ.get('SHODAN_API_KEY')) if os.environ.get('SHODAN_API_KEY') else None
        self.censys_client = censys.search.CensysHosts() if os.environ.get('CENSYS_API_ID') else None

    def scan(self, data: Dict) -> Dict:
        """Perform reconnaissance scan"""
        target = data.get('target')

        if not target:
            return {'error': 'No target specified'}

        # Extract domain
        ext = tldextract.extract(target)
        domain = f"{ext.domain}.{ext.suffix}"

        info = TargetInfo(
            domain=domain,
            ip='',
            nameservers=[],
            mx_records=[],
            technologies=[],
            subdomains=[],
            emails=[]
        )

        # Get IP
        try:
            info.ip = socket.gethostbyname(domain)
        except:
            pass

        # Get WHOIS
        try:
            w = whois.whois(domain)
            info.nameservers = w.name_servers if w.name_servers else []
        except:
            pass

        # Get DNS records
        try:
            mx = dns.resolver.resolve(domain, 'MX')
            info.mx_records = [str(r.exchange) for r in mx]
        except:
            pass

        # Get technologies
        try:
            response = requests.get(f'https://{domain}', timeout=10)
            wapp = wappalyzer.Wappalyzer.latest()
            webpage = wappalyzer.WebPage.new_from_response(response)
            info.technologies = list(wapp.analyze(webpage))
        except:
            pass

        # Shodan search
        if self.shodan_client:
            try:
                results = self.shodan_client.search(f'hostname:{domain}')
                for result in results['matches'][:5]:
                    info.subdomains.append(result['hostnames'][0])
            except:
                pass

        return {
            'domain': info.domain,
            'ip': info.ip,
            'nameservers': info.nameservers,
            'mx_records': info.mx_records,
            'technologies': info.technologies,
            'subdomains': list(set(info.subdomains)),
            'emails': info.emails
        }

    def enumerate_subdomains(self, domain: str) -> List[str]:
        """Enumerate subdomains"""
        subdomains = []
        wordlist = ['www', 'mail', 'ftp', 'admin', 'portal', 'login', 'secure', 'api', 'app']

        for sub in wordlist:
            try:
                full_domain = f"{sub}.{domain}"
                socket.gethostbyname(full_domain)
                subdomains.append(full_domain)
            except:
                pass

        return subdomains

    def find_emails(self, domain: str) -> List[str]:
        """Find email addresses"""
        # This would scrape emails from website
        return []

    def analyze_technologies(self, url: str) -> List[str]:
        """Analyze technologies used"""
        try:
            response = requests.get(url, timeout=10)
            wapp = wappalyzer.Wappalyzer.latest()
            webpage = wappalyzer.WebPage.new_from_response(response)
            return list(wapp.analyze(webpage))
        except:
            return []
