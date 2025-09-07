# Repository Context - 2025-09-06
## DataMint Verticals Integration
- Successfully restored demo version functionality
- Rolled back database integration to hardcoded verticals
- All 15 industry verticals working in DataMint
- API endpoints functional at /api/v1/verticals

## Testing Requirements
- Any changes must have associated tests
- Must validate no regression in overall system
- Testing mandatory before commits/deployments

# IMPORTANT PROJECT STRUCTURE NOTE

## Directory Structure
- /home/dmiruke/agent-dev-products is NOT a git repository
- It is a product development project directory containing 10 separate git repositories
- This repository (inferloop-agentforge) is one of 10 independent git repositories

## Git Repositories in Project:
1. inferloop-agentcraft
2. inferloop-agentforge
3. inferloop-agents
4. inferloop-datalake
5. inferloop-datamint
6. inferloop-designs
7. inferloop-marketplace
8. inferloop-runtime
9. inferloop-testnest
10. inferloop-trustscan

## Current Status
- All repositories are on 'multi_tenant_saas' branch
- Each repository maintains independent git history

## Testing Requirements
- Any changes must have associated tests
- Must validate no regression in overall system
- Testing mandatory before commits/deployments

