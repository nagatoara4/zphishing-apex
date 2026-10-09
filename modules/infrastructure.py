#!/usr/bin/env python3
"""
ZPHISHING APEX — Infrastructure Manager
"""

import os
import json
import time
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass

import docker
from kubernetes import client, config

@dataclass
class InfrastructureDeployment:
    id: str
    provider: str
    status: str
    resources: Dict
    created_at: float

class InfrastructureManager:
    def __init__(self):
        self.deployments = {}
        self.docker_client = docker.from_env()

    def spin(self, data: Dict) -> Dict:
        """Spin up infrastructure"""
        provider = data.get('provider', 'docker')

        if provider == 'docker':
            return self._spin_docker(data)
        elif provider == 'kubernetes':
            return self._spin_kubernetes(data)
        elif provider == 'terraform':
            return self._spin_terraform(data)
        else:
            return {'error': 'Unknown provider'}

    def _spin_docker(self, data: Dict) -> Dict:
        """Spin up Docker infrastructure"""
        try:
            # Build image if needed
            self.docker_client.images.build(
                path='.',
                tag='zphishing:latest',
                rm=True
            )

            # Run container
            container = self.docker_client.containers.run(
                image='zphishing:latest',
                name=f'zphishing-{int(time.time())}',
                ports={'8080/tcp': data.get('port', 8080)},
                detach=True,
                environment={
                    'DATABASE_URL': os.environ.get('DATABASE_URL'),
                    'REDIS_URL': os.environ.get('REDIS_URL')
                }
            )

            deployment_id = f'deploy_{int(time.time())}'

            deployment = InfrastructureDeployment(
                id=deployment_id,
                provider='docker',
                status='running',
                resources={'container_id': container.id},
                created_at=time.time()
            )

            self.deployments[deployment_id] = deployment

            return {
                'id': deployment_id,
                'provider': 'docker',
                'container_id': container.id,
                'status': 'running'
            }
        except Exception as e:
            return {'error': str(e)}

    def _spin_kubernetes(self, data: Dict) -> Dict:
        """Spin up Kubernetes infrastructure"""
        try:
            config.load_kube_config()
            v1 = client.CoreV1Api()

            deployment_id = f'k8s_{int(time.time())}'

            return {
                'id': deployment_id,
                'provider': 'kubernetes',
                'status': 'created'
            }
        except Exception as e:
            return {'error': str(e)}

    def _spin_terraform(self, data: Dict) -> Dict:
        """Spin up infrastructure with Terraform"""
        try:
            result = subprocess.run(
                ['terraform', 'apply', '-auto-approve'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                deployment_id = f'tf_{int(time.time())}'

                return {
                    'id': deployment_id,
                    'provider': 'terraform',
                    'status': 'applied',
                    'output': result.stdout
                }
            else:
                return {'error': result.stderr}
        except Exception as e:
            return {'error': str(e)}

    def destroy(self, data: Dict) -> Dict:
        """Destroy infrastructure"""
        deployment_id = data.get('id')

        if deployment_id not in self.deployments:
            return {'error': 'Deployment not found'}

        deployment = self.deployments[deployment_id]

        if deployment.provider == 'docker':
            try:
                container = self.docker_client.containers.get(
                    deployment.resources['container_id']
                )
                container.stop()
                container.remove()

                deployment.status = 'destroyed'

                return {'status': 'destroyed'}
            except Exception as e:
                return {'error': str(e)}

        return {'error': 'Unknown provider'}

    def list_deployments(self) -> List[Dict]:
        """List all deployments"""
        return [{
            'id': d.id,
            'provider': d.provider,
            'status': d.status,
            'created_at': d.created_at
        } for d in self.deployments.values()]
