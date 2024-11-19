from dataclasses import dataclass
from typing import Dict, Optional
from pathlib import Path
import yaml

@dataclass
class DeploymentConfig:
    provider: str
    region: str
    instance_type: Optional[str] = None
    ami_id: Optional[str] = None

@dataclass
class Configuration:
    project_name: str
    ci_provider: str
    deployment: DeploymentConfig
    environments: Dict[str, Dict[str, str]]
    
    @classmethod
    def from_dict(cls, data: dict):
        deployment_data = data.get('deployment', {})
        deployment = DeploymentConfig(
            provider=deployment_data.get('provider', ''),
            region=deployment_data.get('region', ''),
            instance_type=deployment_data.get('instance_type'),
            ami_id=deployment_data.get('ami_id')
        )
        
        return cls(
            project_name=data.get('project_name', ''),
            ci_provider=data.get('ci_provider', ''),
            deployment=deployment,
            environments=data.get('environments', {})
        )
        
    def to_dict(self) -> dict:
        return {
            'project_name': self.project_name,
            'ci_provider': self.ci_provider,
            'deployment': {
                'provider': self.deployment.provider,
                'region': self.deployment.region,
                'instance_type': self.deployment.instance_type,
                'ami_id': self.deployment.ami_id
            },
            'environments': self.environments
        } 