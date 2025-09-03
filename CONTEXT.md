# Context for InferLoop AgentForge

## Repository Purpose
Comprehensive framework setup and environment management for AI agent development, providing automated installation and configuration for multiple agent frameworks.

## Current Status
- **Phase**: Planning/Early Development
- **Implementation**: Framework adapters being designed
- **Priority**: P3 (Infrastructure component)

## Key Integration Points
- **Supports**: inferloop-agentcraft (provides framework environments)
- **Configures for**: inferloop-testnest (sandbox environments)
- **Validates with**: inferloop-trustscan (framework compatibility)

## Framework Support
Primary frameworks:
- LangChain/LangGraph
- AutoGen (Microsoft)
- CrewAI
- Semantic Kernel
- OpenAI Swarm
- Custom frameworks

## Technology Stack
- Python 3.8-3.12 support
- Virtual environment management
- Docker containerization
- Package management (pip, conda)
- Configuration management

## Testing Requirements
- Zero regression tolerance
- Minimum 80% code coverage
- Compatibility matrix testing
- Multi-version support validation

## Key Features
- Automated framework installation
- Dependency conflict resolution
- Virtual environment isolation
- Configuration templates
- Version management
- Rollback capabilities

## Recent Changes
- Created README.md with framework details
- Added TESTING_REQUIREMENTS.md
- Established compatibility testing matrix

## Next Steps
1. Implement base installer class
2. Create framework-specific adapters
3. Build dependency resolver
4. Implement environment manager
5. Create configuration templates