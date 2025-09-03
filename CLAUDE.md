# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

InferLoop AgentForge is a framework setup and environment preparation tool that serves as the foundation layer for the InferLoop AI Agent Development Ecosystem. It handles framework selection, environment configuration, and boilerplate generation to accelerate agent development.

**Current Status**: Design and Architecture phase

## Development Commands

### AgentForge CLI (Planned)
```bash
# Install AgentForge CLI
pip install inferloop-agentforge

# Initialize new agent project
agentforge init my-agent --framework langchain

# Setup development environment
agentforge setup --env development

# Generate boilerplate code
agentforge generate --template rag-agent

# Benchmark available frameworks
agentforge benchmark --use-case "data-analysis"
```

## High-Level Architecture

### Core Purpose
AgentForge focuses on the foundation layer:
- **Framework Selection**: Benchmark-driven recommendations for choosing the right AI framework
- **Environment Setup**: Automated development environment creation and configuration
- **Boilerplate Generation**: Framework-specific scaffolding and project templates
- **Dependency Management**: Smart package resolution and compatibility checking

### Module Distribution in AgentForge
- **BUILDER Module**: Framework setup, dependency installation, environment configuration, boilerplate generation
- **TESTER Module**: Framework validation, dependency verification, environment health checks, performance benchmarking
- **DEPLOYER Module**: Local development setup, Docker compose configuration, development containers, build script generation
- **MONITOR Module**: Installation progress tracking, dependency status monitoring, environment health monitoring

### Relationship to Other Products
- **AgentForge → AgentCraft**: AgentForge prepares the environment and generates initial code structure, which feeds directly into AgentCraft for visual development and production deployment
- **AgentForge → AgentHub**: Integrates with marketplace to discover/import templates, publish boilerplates, and access community-contributed setups

## Technology Stack

- **Language**: Python 3.11+
- **CLI Framework**: Click/Typer (planned)
- **Container Support**: Docker, Docker Compose
- **Package Management**: Poetry, pip, conda
- **Configuration**: YAML, TOML, environment files
- **Supported AI Frameworks**: LangChain, AutoGen, CrewAI, Semantic Kernel, OpenAI Swarm

## Development Guidelines

### Multi-Framework Support
All agent frameworks should be supported through a common adapter pattern, allowing users to switch between frameworks easily.

### Key Design Principles
1. **Framework Agnostic**: Support all major AI agent frameworks equally
2. **Intelligent Defaults**: Provide smart defaults based on use case and framework benchmarks
3. **Dependency Resolution**: Automatically resolve and manage complex dependency chains
4. **Environment Isolation**: Ensure clean, isolated development environments
5. **Template-Driven**: Use customizable templates for boilerplate generation

## Common Tasks

### Adding New Framework Support
1. Create framework adapter in the adapters directory
2. Define framework-specific dependencies and configuration
3. Add boilerplate templates for the framework
4. Include framework in benchmarking suite
5. Update CLI to recognize new framework option

### Creating New Templates
1. Define template structure in YAML/TOML
2. Create boilerplate code files
3. Add template metadata (description, dependencies, use cases)
4. Register template in template registry
5. Add template tests

## Integration Points

### With InferLoop Ecosystem
- **Input to AgentCraft**: Generated project structure and boilerplate code
- **From AgentHub**: Framework templates and community contributions
- **To TrustScan**: Initial agent code for validation
- **To TestNest**: Development environment configurations

### External Services
- Package registries (PyPI, npm, conda-forge)
- Framework repositories (GitHub)
- Docker Hub for base images
- Cloud provider CLIs for deployment preparation

## Related Documentation

- Parent repository: `/home/dmiruke/agent-dev-products/inferloop-designs/CLAUDE.md`
- Module mapping: `/home/dmiruke/agent-dev-products/inferloop-designs/MODULE_PRODUCT_MAPPING.md`
- AgentCraft integration: `/home/dmiruke/agent-dev-products/inferloop-agentcraft/designs/integration/MODULE_DIFFERENTIATION.md`