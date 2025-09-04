"""
Base Framework Interface for AgentForge
This provides the abstraction layer for managing multiple agent frameworks
while working seamlessly with the inferloop-agents repository.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class Agent:
    """Represents a built agent"""
    id: str
    name: str
    framework: str
    source_code: str
    compiled_code: Optional[str] = None
    dependencies: List[str] = None
    configuration: Dict[str, Any] = None
    deployment_config: Dict[str, Any] = None
    metadata: Dict[str, Any] = None


@dataclass
class BuiltAgent:
    """Represents a fully built and packaged agent"""
    agent: Agent
    package_path: str
    docker_image: Optional[str] = None
    deployment_manifest: Optional[str] = None
    documentation: Optional[str] = None


class BaseAgentFramework(ABC):
    """
    Base interface for all agent frameworks.
    This works with existing agents from inferloop-agents repository.
    """
    
    def __init__(self):
        self.framework_name = self.__class__.__name__.replace('Adapter', '').lower()
        self.supported_features = []
        
    @abstractmethod
    def build_agent(self, source_code: str, config: Dict[str, Any]) -> Agent:
        """
        Build an agent from source code.
        Source code can come from inferloop-agents templates.
        """
        pass
    
    @abstractmethod
    def validate_agent(self, agent: Agent) -> bool:
        """Validate agent configuration and code"""
        pass
    
    @abstractmethod
    def optimize_agent(self, agent: Agent, target: str = 'production') -> Agent:
        """
        Optimize agent for target environment.
        Targets: development, staging, production
        """
        pass
    
    @abstractmethod
    def generate_deployment(self, agent: Agent, platform: str) -> Dict[str, Any]:
        """
        Generate deployment configuration.
        Platforms: kubernetes, docker, aws, azure, gcp
        """
        pass
    
    @abstractmethod
    def translate_to(self, agent: Agent, target_framework: str) -> str:
        """Translate agent to another framework"""
        pass
    
    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """Get framework-specific dependencies"""
        pass
    
    @abstractmethod
    def get_supported_features(self) -> List[str]:
        """Get list of supported features for this framework"""
        pass
    
    def import_from_agents_repo(self, agent_path: str) -> str:
        """
        Import agent code from inferloop-agents repository.
        Preserves existing agent functionality.
        """
        import os
        
        # Support both relative and absolute paths
        if not os.path.isabs(agent_path):
            # Assume relative to inferloop-agents repo
            agents_repo = "/home/dmiruke/agent-dev-products/inferloop-agents"
            agent_path = os.path.join(agents_repo, agent_path)
        
        # Read agent source code
        source_files = []
        src_path = os.path.join(agent_path, "src")
        
        if os.path.exists(src_path):
            for file in os.listdir(src_path):
                if file.endswith('.py'):
                    with open(os.path.join(src_path, file), 'r') as f:
                        source_files.append(f.read())
        
        return "\n\n".join(source_files)
    
    def package_agent(self, agent: Agent, output_format: str = 'standalone') -> BuiltAgent:
        """
        Package agent for distribution.
        Formats: standalone, docker, kubernetes, cloud
        """
        # This will be implemented by specific framework adapters
        pass