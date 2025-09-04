"""
Unified Agent Build System for AgentForge
Works with existing agents from inferloop-agents repository
"""

import os
import json
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import shutil
import subprocess

# Import framework registry
import sys
sys.path.append('/home/dmiruke/agent-dev-products/inferloop-agentforge')
from framework_registry import FrameworkRegistry


class AgentBuilder:
    """
    Builds agents for different frameworks while preserving
    functionality from inferloop-agents repository.
    """
    
    def __init__(self):
        self.registry = FrameworkRegistry()
        self.build_cache = {}
        
    async def build(self,
                    agent_source: str,
                    framework: str,
                    optimization: str = 'balanced',
                    config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Build agent for specified framework.
        
        Args:
            agent_source: Either path to agent in inferloop-agents or raw source code
            framework: Target framework (langchain, crewai, autogen, etc.)
            optimization: Optimization level (development, balanced, production)
            config: Additional configuration
        
        Returns:
            Built agent package
        """
        
        # Check if agent_source is a path to inferloop-agents
        if '/' in agent_source and not agent_source.startswith('/'):
            # It's a relative path like "finance/fraud_detection"
            parts = agent_source.split('/')
            if len(parts) == 2:
                category, agent_name = parts
                return await self.build_from_repo(category, agent_name, framework, optimization, config)
        
        # Otherwise, treat as raw source code
        return await self.build_from_source(agent_source, framework, optimization, config)
    
    async def build_from_repo(self,
                              category: str,
                              agent_name: str,
                              framework: str,
                              optimization: str = 'production',
                              config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Build agent from inferloop-agents repository.
        Preserves all original functionality.
        """
        
        print(f"Building {category}/{agent_name} with {framework} framework...")
        
        # Get agent from repository
        agent_data = self.registry.get_agent_from_repo(category, agent_name)
        
        # Get framework adapter
        adapter = self.registry.get_adapter(framework)
        
        if not adapter:
            # Fallback: package as-is without framework translation
            return await self.package_raw_agent(agent_data)
        
        # Combine source files
        source_code = "\n\n".join([f['content'] for f in agent_data['source_files']])
        
        # Build configuration
        build_config = {
            'agent_id': f"{category}-{agent_name}",
            'name': agent_name.replace('_', ' ').title(),
            'category': category,
            'optimization': optimization
        }
        
        if config:
            build_config.update(config)
        
        # Build with framework
        agent = adapter.build_agent(source_code, build_config)
        
        # Optimize
        if optimization != 'none':
            agent = adapter.optimize_agent(agent, optimization)
        
        # Package
        package = await self.package_agent(agent, agent_data)
        
        return package
    
    async def build_from_source(self,
                                source_code: str,
                                framework: str,
                                optimization: str = 'balanced',
                                config: Optional[Dict] = None) -> Dict[str, Any]:
        """Build agent from raw source code"""
        
        adapter = self.registry.get_adapter(framework)
        
        if not adapter:
            raise ValueError(f"Framework {framework} not supported")
        
        # Default configuration
        build_config = {
            'agent_id': f"custom-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'name': 'Custom Agent',
            'optimization': optimization
        }
        
        if config:
            build_config.update(config)
        
        # Build
        agent = adapter.build_agent(source_code, build_config)
        
        # Optimize
        if optimization != 'none':
            agent = adapter.optimize_agent(agent, optimization)
        
        # Package
        package = await self.package_agent(agent, None)
        
        return package
    
    async def package_agent(self, agent: Any, agent_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Package agent for deployment.
        Maintains compatibility with inferloop-agents structure.
        """
        
        # Create package directory
        package_dir = f"/tmp/agent-package-{agent.id}"
        os.makedirs(package_dir, exist_ok=True)
        
        # Create standard structure
        dirs = ['src', 'tests', 'config', 'deployment', 'docs']
        for dir_name in dirs:
            os.makedirs(os.path.join(package_dir, dir_name), exist_ok=True)
        
        # Write agent code
        with open(os.path.join(package_dir, 'src', 'agent.py'), 'w') as f:
            f.write(agent.compiled_code or agent.source_code)
        
        # Write requirements
        with open(os.path.join(package_dir, 'requirements.txt'), 'w') as f:
            f.write('\n'.join(agent.dependencies or []))
        
        # Write configuration
        with open(os.path.join(package_dir, 'config', 'agent_config.json'), 'w') as f:
            json.dump(agent.configuration or {}, f, indent=2)
        
        # Copy original files if available
        if agent_data and 'path' in agent_data:
            original_path = agent_data['path']
            
            # Copy tests if they exist
            test_path = os.path.join(original_path, 'tests')
            if os.path.exists(test_path):
                shutil.copytree(test_path, os.path.join(package_dir, 'tests'), dirs_exist_ok=True)
            
            # Copy docs
            doc_files = ['README.md', 'architecture.md', 'IMPLEMENTATION_GUIDE.md']
            for doc in doc_files:
                doc_path = os.path.join(original_path, doc)
                if os.path.exists(doc_path):
                    shutil.copy(doc_path, os.path.join(package_dir, 'docs'))
        
        # Generate deployment files
        deployment_config = agent.deployment_config or {}
        
        # Docker
        dockerfile = deployment_config.get('dockerfile', self.generate_dockerfile(agent))
        with open(os.path.join(package_dir, 'deployment', 'Dockerfile'), 'w') as f:
            f.write(dockerfile)
        
        # Docker Compose
        compose = deployment_config.get('compose', self.generate_compose(agent))
        with open(os.path.join(package_dir, 'deployment', 'docker-compose.yml'), 'w') as f:
            import yaml
            yaml.dump(compose, f)
        
        # Create package metadata
        metadata = {
            'agent_id': agent.id,
            'name': agent.name,
            'framework': agent.framework,
            'created_at': datetime.now().isoformat(),
            'package_path': package_dir,
            'files': os.listdir(package_dir)
        }
        
        with open(os.path.join(package_dir, 'package.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            'success': True,
            'package_path': package_dir,
            'metadata': metadata,
            'agent': agent
        }
    
    async def package_raw_agent(self, agent_data: Dict) -> Dict[str, Any]:
        """
        Package agent without framework translation.
        Used when framework adapter is not available.
        """
        
        package_dir = f"/tmp/agent-package-{agent_data['category']}-{agent_data['name']}"
        os.makedirs(package_dir, exist_ok=True)
        
        # Copy all files from original agent
        if os.path.exists(agent_data['path']):
            shutil.copytree(agent_data['path'], package_dir, dirs_exist_ok=True)
        
        # Add package metadata
        metadata = {
            'agent_id': f"{agent_data['category']}-{agent_data['name']}",
            'name': agent_data['name'],
            'category': agent_data['category'],
            'framework': 'original',
            'created_at': datetime.now().isoformat(),
            'package_path': package_dir
        }
        
        with open(os.path.join(package_dir, 'package.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            'success': True,
            'package_path': package_dir,
            'metadata': metadata,
            'warning': 'Packaged without framework translation'
        }
    
    def generate_dockerfile(self, agent: Any) -> str:
        """Generate default Dockerfile"""
        return f"""
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY src/ ./src/
COPY config/ ./config/

# Set environment variables
ENV AGENT_ID={agent.id}
ENV AGENT_FRAMEWORK={agent.framework}

# Run agent
CMD ["python", "src/agent.py"]
"""
    
    def generate_compose(self, agent: Any) -> Dict:
        """Generate default docker-compose.yml"""
        return {
            'version': '3.8',
            'services': {
                agent.id: {
                    'build': '.',
                    'container_name': agent.id,
                    'ports': ['8000:8000'],
                    'environment': {
                        'AGENT_ID': agent.id,
                        'AGENT_FRAMEWORK': agent.framework
                    },
                    'restart': 'unless-stopped'
                }
            }
        }


# Convenience functions

async def build_agent(agent_path: str, framework: str, **kwargs):
    """
    Build an agent with specified framework.
    
    Examples:
        # From inferloop-agents repository
        agent = await build_agent('finance/fraud_detection', 'langchain')
        
        # From source code
        agent = await build_agent(source_code, 'crewai')
    """
    builder = AgentBuilder()
    return await builder.build(agent_path, framework, **kwargs)


async def build_from_repo(category: str, name: str, framework: str, **kwargs):
    """
    Build agent from inferloop-agents repository.
    
    Example:
        agent = await build_from_repo('finance', 'fraud_detection', 'langchain')
    """
    builder = AgentBuilder()
    return await builder.build_from_repo(category, name, framework, **kwargs)