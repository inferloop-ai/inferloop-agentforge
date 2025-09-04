"""
Framework Registry for AgentForge
Central registry of all supported frameworks with connections to inferloop-agents
"""

import os
import importlib
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class FrameworkInfo:
    """Information about a framework"""
    name: str
    version: str
    adapter_module: str
    requirements: list
    supported_features: list
    description: str


class FrameworkRegistry:
    """
    Central registry of all supported frameworks.
    Works with agents from inferloop-agents repository.
    """
    
    FRAMEWORKS = {
        'langchain': FrameworkInfo(
            name='langchain',
            version='0.1.0',
            adapter_module='framework_adapters.langchain.adapter.LangChainAdapter',
            requirements=['langchain>=0.1.0', 'openai'],
            supported_features=['rag', 'tools', 'memory', 'streaming', 'async'],
            description='LangChain framework for building LLM applications'
        ),
        'crewai': FrameworkInfo(
            name='crewai',
            version='0.1.0',
            adapter_module='framework_adapters.crewai.adapter.CrewAIAdapter',
            requirements=['crewai>=0.1.0'],
            supported_features=['multi-agent', 'delegation', 'tools', 'roles'],
            description='CrewAI for multi-agent systems with role-based collaboration'
        ),
        'autogen': FrameworkInfo(
            name='autogen',
            version='0.2.0',
            adapter_module='framework_adapters.autogen.adapter.AutoGenAdapter',
            requirements=['pyautogen>=0.2.0'],
            supported_features=['multi-agent', 'code-generation', 'conversation', 'tools'],
            description='Microsoft AutoGen for multi-agent conversations'
        ),
        'langgraph': FrameworkInfo(
            name='langgraph',
            version='0.0.20',
            adapter_module='framework_adapters.langgraph.adapter.LangGraphAdapter',
            requirements=['langgraph>=0.0.20'],
            supported_features=['stateful', 'graphs', 'cycles', 'conditional'],
            description='LangGraph for stateful, graph-based agent workflows'
        ),
        'langsmith': FrameworkInfo(
            name='langsmith',
            version='0.1.0',
            adapter_module='framework_adapters.langsmith.adapter.LangSmithAdapter',
            requirements=['langsmith>=0.1.0'],
            supported_features=['tracing', 'evaluation', 'monitoring', 'debugging'],
            description='LangSmith for LLM application monitoring and testing'
        ),
        'openai-swarm': FrameworkInfo(
            name='openai-swarm',
            version='0.1.0',
            adapter_module='framework_adapters.openai_swarm.adapter.SwarmAdapter',
            requirements=['openai>=1.0.0'],
            supported_features=['lightweight', 'educational', 'multi-agent'],
            description='OpenAI Swarm experimental multi-agent framework'
        ),
        'semantic-kernel': FrameworkInfo(
            name='semantic-kernel',
            version='0.9.0',
            adapter_module='framework_adapters.semantic_kernel.adapter.SemanticKernelAdapter',
            requirements=['semantic-kernel>=0.9.0'],
            supported_features=['plugins', 'planners', 'memory', 'connectors'],
            description='Microsoft Semantic Kernel for AI orchestration'
        ),
        'metagpt': FrameworkInfo(
            name='metagpt',
            version='0.7.0',
            adapter_module='framework_adapters.metagpt.adapter.MetaGPTAdapter',
            requirements=['metagpt>=0.7.0'],
            supported_features=['software-development', 'multi-agent', 'roles'],
            description='MetaGPT for multi-agent software development'
        ),
        'llamaindex': FrameworkInfo(
            name='llamaindex',
            version='0.10.0',
            adapter_module='framework_adapters.llamaindex.adapter.LlamaIndexAdapter',
            requirements=['llama-index>=0.10.0'],
            supported_features=['rag', 'indexing', 'retrieval', 'query'],
            description='LlamaIndex for LLM data integration'
        ),
        'haystack': FrameworkInfo(
            name='haystack',
            version='2.0.0',
            adapter_module='framework_adapters.haystack.adapter.HaystackAdapter',
            requirements=['haystack-ai>=2.0.0'],
            supported_features=['pipelines', 'rag', 'search', 'qa'],
            description='Haystack for building NLP pipelines'
        ),
        'vertexai': FrameworkInfo(
            name='vertexai',
            version='1.0.0',
            adapter_module='framework_adapters.vertexai.adapter.VertexAIAdapter',
            requirements=['google-cloud-aiplatform>=1.0.0'],
            supported_features=['google-models', 'enterprise', 'scaling'],
            description='Google Vertex AI for enterprise AI'
        ),
        'bedrock': FrameworkInfo(
            name='bedrock',
            version='1.0.0',
            adapter_module='framework_adapters.bedrock.adapter.BedrockAdapter',
            requirements=['boto3>=1.28.0'],
            supported_features=['aws-models', 'enterprise', 'security'],
            description='AWS Bedrock for foundation models'
        ),
        'azure-ai': FrameworkInfo(
            name='azure-ai',
            version='1.0.0',
            adapter_module='framework_adapters.azure_ai.adapter.AzureAIAdapter',
            requirements=['azure-ai-ml>=1.0.0'],
            supported_features=['azure-models', 'enterprise', 'integration'],
            description='Azure AI for Microsoft cloud AI services'
        ),
        'custom': FrameworkInfo(
            name='custom',
            version='1.0.0',
            adapter_module='framework_adapters.custom.adapter.CustomAdapter',
            requirements=[],
            supported_features=['flexible', 'extensible'],
            description='Custom framework adapter for proprietary implementations'
        )
    }
    
    # Path to inferloop-agents repository
    AGENTS_REPO_PATH = '/home/dmiruke/agent-dev-products/inferloop-agents'
    
    @classmethod
    def get_framework(cls, name: str) -> FrameworkInfo:
        """Get framework information by name"""
        if name not in cls.FRAMEWORKS:
            raise ValueError(f"Framework {name} not supported. Available: {list(cls.FRAMEWORKS.keys())}")
        return cls.FRAMEWORKS[name]
    
    @classmethod
    def list_frameworks(cls) -> list:
        """List all available frameworks"""
        return list(cls.FRAMEWORKS.keys())
    
    @classmethod
    def get_adapter(cls, framework_name: str):
        """
        Get framework adapter instance.
        Dynamically imports and instantiates the adapter.
        """
        framework = cls.get_framework(framework_name)
        
        # Parse module and class names
        module_path, class_name = framework.adapter_module.rsplit('.', 1)
        
        try:
            # Import the module
            module = importlib.import_module(module_path)
            
            # Get the adapter class
            adapter_class = getattr(module, class_name)
            
            # Return an instance
            return adapter_class()
            
        except (ImportError, AttributeError) as e:
            # If adapter doesn't exist yet, return None
            # This allows gradual implementation of adapters
            print(f"Warning: Adapter for {framework_name} not yet implemented: {e}")
            return None
    
    @classmethod
    def get_agent_from_repo(cls, category: str, agent_name: str) -> Dict[str, Any]:
        """
        Get agent template from inferloop-agents repository.
        Preserves existing functionality.
        """
        agent_path = os.path.join(cls.AGENTS_REPO_PATH, 'archived', 'old-agents', category, agent_name)
        
        if not os.path.exists(agent_path):
            # Try new structure
            agent_path = os.path.join(cls.AGENTS_REPO_PATH, 'agentic-frameworks', 'agents-catalog', category, agent_name)
        
        if not os.path.exists(agent_path):
            raise ValueError(f"Agent {category}/{agent_name} not found in repository")
        
        # Read agent files
        agent_data = {
            'category': category,
            'name': agent_name,
            'path': agent_path,
            'source_files': [],
            'config': {},
            'requirements': []
        }
        
        # Read source files
        src_path = os.path.join(agent_path, 'src')
        if os.path.exists(src_path):
            for file in os.listdir(src_path):
                if file.endswith('.py'):
                    file_path = os.path.join(src_path, file)
                    with open(file_path, 'r') as f:
                        agent_data['source_files'].append({
                            'name': file,
                            'content': f.read()
                        })
        
        # Read requirements
        req_file = os.path.join(agent_path, 'requirements.txt')
        if os.path.exists(req_file):
            with open(req_file, 'r') as f:
                agent_data['requirements'] = f.read().strip().split('\n')
        
        # Read config if exists
        config_file = os.path.join(agent_path, 'agent.yaml')
        if os.path.exists(config_file):
            import yaml
            with open(config_file, 'r') as f:
                agent_data['config'] = yaml.safe_load(f)
        
        return agent_data
    
    @classmethod
    def build_agent_with_framework(cls, 
                                    agent_category: str,
                                    agent_name: str,
                                    target_framework: str,
                                    config: Optional[Dict] = None) -> Any:
        """
        Build an agent from inferloop-agents repository with specified framework.
        This is the main integration point between repos.
        """
        
        # Get agent from repository
        agent_data = cls.get_agent_from_repo(agent_category, agent_name)
        
        # Get framework adapter
        adapter = cls.get_adapter(target_framework)
        
        if not adapter:
            raise ValueError(f"Framework {target_framework} adapter not available")
        
        # Combine source files
        source_code = "\n\n".join([f['content'] for f in agent_data['source_files']])
        
        # Merge configurations
        build_config = agent_data['config'] or {}
        if config:
            build_config.update(config)
        
        # Build with framework
        built_agent = adapter.build_agent(source_code, build_config)
        
        # Optimize for production
        optimized = adapter.optimize_agent(built_agent, 'production')
        
        return optimized


# Convenience functions for easy access

def list_available_frameworks():
    """List all available frameworks"""
    return FrameworkRegistry.list_frameworks()


def get_framework_info(name: str):
    """Get information about a specific framework"""
    return FrameworkRegistry.get_framework(name)


def build_agent(agent_category: str, agent_name: str, framework: str, config: Dict = None):
    """
    Build an agent from inferloop-agents with specified framework.
    
    Example:
        agent = build_agent('finance', 'fraud_detection', 'langchain')
    """
    return FrameworkRegistry.build_agent_with_framework(
        agent_category,
        agent_name,
        framework,
        config
    )