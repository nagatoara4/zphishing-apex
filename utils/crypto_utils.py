#!/usr/bin/env python3
"""
ZPHISHING APEX — Crypto Utils
"""

import os
import base64
import hashlib
from typing import Tuple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class CryptoUtils:
    def __init__(self):
        self.backend = default_backend()

    def hash_password(self, password: str) -> str:
        """Hash password"""
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
        """Verify password"""
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

    def generate_token(self, length: int = 32) -> str:
        """Generate random token"""
        return base64.urlsafe_b64encode(os.urandom(length)).decode()

    def hash_data(self, data: str) -> str:
        """Hash data"""
        return hashlib.sha256(data.encode()).hexdigest()

    def encrypt(self, data: str) -> str:
        """Encrypt data"""
        # Simple base64 encoding for now
        return base64.b64encode(data.encode()).decode()
