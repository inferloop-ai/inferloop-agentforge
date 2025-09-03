# Testing Requirements for InferLoop AgentForge

## Zero Regression Policy

**IMPORTANT**: Any change in this repository must have associated tests that ensure absolutely no regression in functionality.

## Testing Strategy

### 1. Unit Tests
- **Coverage Target**: Minimum 80% code coverage
- **Framework**: pytest for Python, Jest for TypeScript
- **Location**: `tests/unit/` directory
- **Naming Convention**: `test_*.py` or `*.test.ts`

### 2. Integration Tests
- **Framework Installation**: Test all supported frameworks
- **Environment Setup**: Verify virtual environments
- **Dependency Resolution**: Test package conflicts
- **Configuration**: Test framework-specific configs

### 3. Compatibility Tests
- **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Node Versions**: 16.x, 18.x, 20.x
- **Framework Versions**: Test latest and LTS versions
- **OS Compatibility**: Linux, macOS, Windows

### 4. Environment Tests
- **Virtual Environment**: Test creation and activation
- **Docker Containers**: Test containerized environments
- **Cloud Environments**: Test AWS, Azure, GCP setups
- **Resource Limits**: Test with constrained resources

## Pre-Commit Requirements

Before committing any changes:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agentforge --cov-report=html

# Run linting
ruff check .
black --check .

# Run type checking
mypy agentforge/

# Run security checks
bandit -r agentforge/
```

## Framework-Specific Testing

### LangChain Setup
```python
def test_langchain_installation():
    # Test package installation
    # Test OPENAI_API_KEY configuration
    # Test basic chain creation
```

### AutoGen Setup
```python
def test_autogen_installation():
    # Test package installation
    # Test Azure OpenAI configuration
    # Test agent initialization
```

### CrewAI Setup
```python
def test_crewai_installation():
    # Test package installation
    # Test crew configuration
    # Test role setup
```

### Semantic Kernel Setup
```python
def test_semantic_kernel_installation():
    # Test package installation
    # Test kernel initialization
    # Test skill registration
```

## Environment Validation Tests

```bash
# Test environment setup
./scripts/test-environment.sh

# Test framework installations
./scripts/test-frameworks.sh

# Test dependency conflicts
./scripts/test-dependencies.sh

# Test resource allocation
./scripts/test-resources.sh
```

## Continuous Integration

All PRs must pass:
- ✅ All unit tests
- ✅ Integration tests
- ✅ Compatibility matrix
- ✅ Code coverage > 80%
- ✅ No linting errors
- ✅ Security scan clean
- ✅ Documentation build

## Regression Prevention

1. **Baseline Tests**: Establish baseline for all frameworks
2. **Version Locking**: Test with locked dependency versions
3. **Upgrade Testing**: Test framework upgrades separately
4. **Rollback Testing**: Ensure rollback procedures work

## Performance Testing

```python
# Test setup time
def test_framework_setup_performance():
    assert setup_time < 30  # seconds

# Test memory usage
def test_memory_consumption():
    assert memory_usage < 500  # MB

# Test concurrent setups
def test_concurrent_installations():
    assert can_handle_parallel_setups(count=5)
```

## Testing Commands

```bash
# Run all tests
make test

# Run unit tests only
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run specific framework tests
pytest -k "langchain"

# Run with verbose output
pytest -v

# Run with parallel execution
pytest -n auto
```

## Cross-Repository Testing

When changes affect other repositories:

1. Test with inferloop-agentcraft for development environment
2. Test with inferloop-testnest for sandbox integration
3. Run full integration suite: `./test-integrations.sh`

## Test Environment Management

```yaml
# test-environments.yaml
environments:
  minimal:
    python: "3.8"
    frameworks: ["langchain"]
  
  standard:
    python: "3.10"
    frameworks: ["langchain", "autogen", "crewai"]
  
  complete:
    python: "3.11"
    frameworks: ["all"]
```

## Error Handling Tests

- Test invalid configurations
- Test missing dependencies
- Test network failures
- Test permission errors
- Test resource exhaustion

## Documentation Tests

```bash
# Test code examples in docs
pytest --doctest-modules

# Test README examples
pytest --doctest-glob="*.md"

# Test installation instructions
./scripts/test-docs.sh
```

## Security Testing

- No hardcoded credentials
- Secure environment variable handling
- Safe package installation
- Vulnerability scanning

---

**Remember**: Zero regression tolerance. Every change must be validated through comprehensive testing.