"""
LangChain Framework Adapter for AgentForge
Builds and manages LangChain-based agents from inferloop-agents templates
"""

import os
import json
from typing import Dict, Any, List
import sys

# Add framework abstractions to path
sys.path.append('/home/dmiruke/agent-dev-products/inferloop-agentforge')

from framework_abstractions.base import BaseAgentFramework, Agent, BuiltAgent


class LangChainAdapter(BaseAgentFramework):
    """LangChain framework adapter"""
    
    def __init__(self):
        super().__init__()
        self.framework_name = 'langchain'
        self.supported_features = [
            'rag',
            'tools',
            'memory',
            'streaming',
            'async',
            'chains',
            'agents',
            'callbacks',
            'embeddings',
            'llm_integration'
        ]
    
    def build_agent(self, source_code: str, config: Dict[str, Any]) -> Agent:
        """
        Build a LangChain agent from source code.
        Can use existing agents from inferloop-agents repository.
        """
        
        # Parse source code to identify LangChain components
        components = self._parse_langchain_components(source_code)
        
        # Generate optimized LangChain code
        optimized_code = self._generate_langchain_code(components, config)
        
        # Create agent object
        agent = Agent(
            id=config.get('agent_id', 'langchain-agent'),
            name=config.get('name', 'LangChain Agent'),
            framework='langchain',
            source_code=source_code,
            compiled_code=optimized_code,
            dependencies=self.get_dependencies(),
            configuration=config,
            deployment_config=self._generate_deployment_config(config),
            metadata={
                'components': components,
                'version': '0.1.0',
                'features': self.supported_features
            }
        )
        
        return agent
    
    def validate_agent(self, agent: Agent) -> bool:
        """Validate LangChain agent configuration"""
        
        # Check required components
        if not agent.compiled_code:
            return False
        
        # Validate LangChain-specific requirements
        required_imports = [
            'from langchain',
            'import langchain'
        ]
        
        has_imports = any(imp in agent.compiled_code for imp in required_imports)
        
        # Check for valid chain or agent definition
        has_chain = 'Chain' in agent.compiled_code or 'Agent' in agent.compiled_code
        
        return has_imports and has_chain
    
    def optimize_agent(self, agent: Agent, target: str = 'production') -> Agent:
        """Optimize LangChain agent for target environment"""
        
        optimizations = {
            'development': {
                'verbose': True,
                'cache': False,
                'streaming': True
            },
            'staging': {
                'verbose': False,
                'cache': True,
                'streaming': True
            },
            'production': {
                'verbose': False,
                'cache': True,
                'streaming': True,
                'batching': True,
                'async': True
            }
        }
        
        # Apply optimizations
        opt_config = optimizations.get(target, optimizations['production'])
        agent.configuration.update(opt_config)
        
        # Update compiled code with optimizations
        agent.compiled_code = self._apply_optimizations(agent.compiled_code, opt_config)
        
        return agent
    
    def generate_deployment(self, agent: Agent, platform: str) -> Dict[str, Any]:
        """Generate LangChain deployment configuration"""
        
        deployments = {
            'docker': self._generate_docker_deployment(agent),
            'kubernetes': self._generate_k8s_deployment(agent),
            'aws': self._generate_aws_deployment(agent),
            'azure': self._generate_azure_deployment(agent),
            'gcp': self._generate_gcp_deployment(agent)
        }
        
        return deployments.get(platform, deployments['docker'])
    
    def translate_to(self, agent: Agent, target_framework: str) -> str:
        """Translate LangChain agent to another framework"""
        
        translators = {
            'crewai': self._translate_to_crewai,
            'autogen': self._translate_to_autogen,
            'langgraph': self._translate_to_langgraph
        }
        
        translator = translators.get(target_framework)
        if not translator:
            raise ValueError(f"Translation from langchain to {target_framework} not supported")
        
        return translator(agent)
    
    def get_dependencies(self) -> List[str]:
        """Get LangChain dependencies"""
        return [
            'langchain>=0.1.0',
            'langchain-community>=0.0.10',
            'langchain-openai>=0.0.5',
            'openai>=1.0.0',
            'tiktoken>=0.5.0',
            'faiss-cpu>=1.7.4',
            'beautifulsoup4>=4.12.0',
            'python-dotenv>=1.0.0'
        ]
    
    def get_supported_features(self) -> List[str]:
        """Get LangChain supported features"""
        return self.supported_features
    
    # Private helper methods
    
    def _parse_langchain_components(self, source_code: str) -> Dict[str, Any]:
        """Parse source code to identify LangChain components"""
        components = {
            'chains': [],
            'agents': [],
            'tools': [],
            'memory': None,
            'callbacks': [],
            'embeddings': None,
            'llm': None
        }
        
        # Simple parsing logic (can be enhanced)
        lines = source_code.split('\n')
        for line in lines:
            if 'Chain' in line and 'class' in line:
                components['chains'].append(line)
            elif 'Agent' in line and 'class' in line:
                components['agents'].append(line)
            elif 'Tool' in line or 'tool' in line:
                components['tools'].append(line)
            elif 'Memory' in line:
                components['memory'] = line
            elif 'Embedding' in line:
                components['embeddings'] = line
            elif 'ChatOpenAI' in line or 'OpenAI' in line:
                components['llm'] = line
        
        return components
    
    def _generate_langchain_code(self, components: Dict, config: Dict) -> str:
        """Generate optimized LangChain code"""
        
        code = """
# Auto-generated LangChain Agent Code
# Built by AgentForge from inferloop-agents template

import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class LangChainAgent:
    def __init__(self, config):
        self.config = config
        self.llm = ChatOpenAI(
            model=config.get('model', 'gpt-4'),
            temperature=config.get('temperature', 0.7)
        )
        self.memory = ConversationBufferMemory()
        self.tools = self._initialize_tools()
        self.agent = self._initialize_agent()
    
    def _initialize_tools(self):
        # Initialize tools based on configuration
        tools = []
        return tools
    
    def _initialize_agent(self):
        return initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=self.config.get('verbose', False)
        )
    
    def run(self, input_text):
        return self.agent.run(input_text)
"""
        return code
    
    def _apply_optimizations(self, code: str, optimizations: Dict) -> str:
        """Apply optimizations to the code"""
        
        # Add optimization flags
        if optimizations.get('async'):
            code = code.replace('def run(', 'async def run(')
        
        if optimizations.get('cache'):
            code = "from langchain.cache import InMemoryCache\n" + code
            code += "\nlangchain.llm_cache = InMemoryCache()\n"
        
        return code
    
    def _generate_docker_deployment(self, agent: Agent) -> Dict[str, Any]:
        """Generate Docker deployment configuration"""
        return {
            'dockerfile': f"""
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
""",
            'requirements': '\n'.join(self.get_dependencies()),
            'compose': {
                'version': '3.8',
                'services': {
                    agent.id: {
                        'build': '.',
                        'ports': ['8000:8000'],
                        'environment': {
                            'OPENAI_API_KEY': '${OPENAI_API_KEY}'
                        }
                    }
                }
            }
        }
    
    def _generate_k8s_deployment(self, agent: Agent) -> Dict[str, Any]:
        """Generate Kubernetes deployment"""
        return {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': agent.id
            },
            'spec': {
                'replicas': 3,
                'selector': {
                    'matchLabels': {
                        'app': agent.id
                    }
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': agent.id
                        }
                    },
                    'spec': {
                        'containers': [{
                            'name': agent.id,
                            'image': f'{agent.id}:latest',
                            'ports': [{'containerPort': 8000}]
                        }]
                    }
                }
            }
        }
    
    def _generate_aws_deployment(self, agent: Agent) -> Dict[str, Any]:
        """Generate AWS deployment configuration"""
        return {
            'service': 'AWS Lambda',
            'runtime': 'python3.10',
            'handler': 'lambda_function.lambda_handler',
            'timeout': 300,
            'memory': 512
        }
    
    def _generate_azure_deployment(self, agent: Agent) -> Dict[str, Any]:
        """Generate Azure deployment configuration"""
        return {
            'service': 'Azure Functions',
            'runtime': 'python',
            'version': '3.10'
        }
    
    def _generate_gcp_deployment(self, agent: Agent) -> Dict[str, Any]:
        """Generate GCP deployment configuration"""
        return {
            'service': 'Cloud Functions',
            'runtime': 'python310',
            'entryPoint': 'main'
        }
    
    def _translate_to_crewai(self, agent: Agent) -> str:
        """Translate to CrewAI"""
        # Translation logic would go here
        return "# CrewAI translation not yet implemented"
    
    def _translate_to_autogen(self, agent: Agent) -> str:
        """Translate to AutoGen"""
        # Translation logic would go here
        return "# AutoGen translation not yet implemented"
    
    def _translate_to_langgraph(self, agent: Agent) -> str:
        """Translate to LangGraph"""
        # Translation logic would go here
        return "# LangGraph translation not yet implemented"