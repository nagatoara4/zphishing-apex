#!/usr/bin/env python3
"""
ZPHISHING APEX — Quantum-Resistant Cryptography
Uses REAL post-quantum algorithms (Kyber, Dilithium)
"""

import os
import json
import base64
from typing import Dict, Tuple, Optional
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import nacl.secret
import nacl.utils

# Try to import post-quantum libraries
try:
    from pqcrypto.kem.kyber512 import generate_keypair as kyber_generate, encrypt as kyber_encrypt, decrypt as kyber_decrypt
    from pqcrypto.sign.dilithium2 import generate_keypair as dilithium_generate, sign as dilithium_sign, verify as dilithium_verify
    PQ_AVAILABLE = True
except ImportError:
    PQ_AVAILABLE = False
    print("WARNING: Post-quantum libraries not available, falling back to classical crypto")

class QuantumCrypto:
    """
    Real post-quantum encryption using Kyber KEM and Dilithium signatures.
    Falls back to RSA-4096 + AES-256-GCM if PQ libraries not available.
    """

    def __init__(self, key_file: Optional[str] = None):
        self.backend = default_backend()
        self.key_file = key_file or "data/quantum_keys.json"

        if PQ_AVAILABLE:
            self._init_pq_keys()
        else:
            self._init_classical_keys()

    def _init_pq_keys(self):
        """Initialize post-quantum keys"""
        if os.path.exists(self.key_file):
            # Load existing keys
            with open(self.key_file, 'r') as f:
                keys = json.load(f)
                self.kyber_secret = base64.b64decode(keys['kyber_secret'])
                self.kyber_public = base64.b64decode(keys['kyber_public'])
                self.dilithium_secret = base64.b64decode(keys['dilithium_secret'])
                self.dilithium_public = base64.b64decode(keys['dilithium_public'])
        else:
            # Generate new keys
            self.kyber_public, self.kyber_secret = kyber_generate()
            self.dilithium_public, self.dilithium_secret = dilithium_generate()

            # Save keys
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            with open(self.key_file, 'w') as f:
                json.dump({
                    'kyber_secret': base64.b64encode(self.kyber_secret).decode(),
                    'kyber_public': base64.b64encode(self.kyber_public).decode(),
                    'dilithium_secret': base64.b64encode(self.dilithium_secret).decode(),
                    'dilithium_public': base64.b64encode(self.dilithium_public).decode()
                }, f)

    def _init_classical_keys(self):
        """Initialize classical keys (fallback)"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'r') as f:
                keys = json.load(f)
                self.private_key = serialization.load_pem_private_key(
                    base64.b64decode(keys['rsa_private']),
                    password=None,
                    backend=self.backend
                )
                self.public_key = self.private_key.public_key()
        else:
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,
                backend=self.backend
            )
            self.public_key = self.private_key.public_key()

            # Save keys
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            pem_private = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(self.key_file, 'w') as f:
                json.dump({
                    'rsa_private': base64.b64encode(pem_private).decode()
                }, f)

    def encrypt(self, data: str) -> str:
        """
        Encrypt data with post-quantum Kyber KEM.
        Returns base64-encoded ciphertext.
        """
        if PQ_AVAILABLE:
            # Use Kyber KEM
            ciphertext, shared_secret = kyber_encrypt(self.kyber_public)

            # Use shared secret for symmetric encryption
            box = nacl.secret.SecretBox(shared_secret[:32])
            encrypted_data = box.encrypt(data.encode())

            # Combine: Kyber ciphertext + encrypted data
            combined = ciphertext + encrypted_data
            return base64.b64encode(combined).decode()
        else:
            # Fallback: RSA-OAEP + NaCl
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

            combined = encrypted_key + encrypted_data
            return base64.b64encode(combined).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt data with post-quantum Kyber KEM.
        """
        combined = base64.b64decode(encrypted_data.encode())

        if PQ_AVAILABLE:
            # Kyber ciphertext size is 768 bytes
            kyber_ct_size = 768
            ciphertext = combined[:kyber_ct_size]
            encrypted_message = combined[kyber_ct_size:]

            # Decapsulate shared secret
            shared_secret = kyber_decrypt(ciphertext, self.kyber_secret)

            # Decrypt data
            box = nacl.secret.SecretBox(shared_secret[:32])
            decrypted = box.decrypt(encrypted_message)
            return decrypted.decode()
        else:
            # Fallback: RSA-OAEP
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
            decrypted = box.decrypt(encrypted_message)
            return decrypted.decode()

    def sign(self, data: str) -> str:
        """Sign data with Dilithium (post-quantum signature)"""
        if PQ_AVAILABLE:
            signature = dilithium_sign(self.dilithium_secret, data.encode())
            return base64.b64encode(signature).decode()
        else:
            # Fallback: HMAC
            import hmac
            key = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            signature = hmac.new(key[:32], data.encode(), hashes.SHA256()).digest()
            return base64.b64encode(signature).decode()

    def verify(self, data: str, signature: str) -> bool:
        """Verify signature"""
        if PQ_AVAILABLE:
            try:
                sig = base64.b64decode(signature.encode())
                dilithium_verify(self.dilithium_public, data.encode(), sig)
                return True
            except:
                return False
        else:
            import hmac
            key = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            expected = hmac.new(key[:32], data.encode(), hashes.SHA256()).digest()
            return hmac.compare_digest(expected, base64.b64decode(signature.encode()))

    def hash_password(self, password: str) -> str:
        """Hash password with Argon2id"""
        from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

        salt = os.urandom(16)
        kdf = Argon2id(
            salt=salt,
            length=32,
            iterations=3,
            lanes=4,
            memory_cost=65536,
            ad=None,
            backend=self.backend
        )
        key = kdf.derive(password.encode())
        return base64.b64encode(salt + key).decode()

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against Argon2id hash"""
        from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

        decoded = base64.b64decode(hashed.encode())
        salt = decoded[:16]
        key = decoded[16:]

        kdf = Argon2id(
            salt=salt,
            length=32,
            iterations=3,
            lanes=4,
            memory_cost=65536,
            ad=None,
            backend=self.backend
        )

        try:
            kdf.verify(password.encode(), key)
            return True
        except Exception:
            return False

    def get_public_key_pem(self) -> str:
        """Get public key info"""
        if PQ_AVAILABLE:
            return {
                'type': 'Kyber512 + Dilithium2',
                'kyber_public': base64.b64encode(self.kyber_public).decode()[:64] + '...',
                'dilithium_public': base64.b64encode(self.dilithium_public).decode()[:64] + '...'
            }
        else:
            pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            return pem.decode()
