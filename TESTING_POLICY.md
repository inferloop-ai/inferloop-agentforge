# Inferloop Testing Policy
## MANDATORY FOR ALL REPOSITORIES

**Effective Date**: September 3, 2025  
**Policy Version**: 1.0  
**Enforcement**: MANDATORY - No exceptions

---

## 🚨 CRITICAL REQUIREMENT

**EVERY CHANGE, NO MATTER HOW SMALL, MUST HAVE ASSOCIATED TESTS**

This policy applies to:
- All Inferloop repositories
- All code changes (features, fixes, refactoring)
- All configuration changes
- All documentation that includes code examples

---

## Core Testing Principles

### 1. Zero Regression Tolerance
- **NO** functionality should break with new changes
- **NO** existing tests should fail after changes
- **NO** deployment without passing all tests

### 2. Test-First Development
Before implementing any change:
1. Write tests that define expected behavior
2. Ensure tests fail initially (red)
3. Implement the change
4. Ensure tests pass (green)
5. Refactor if needed (maintain green)

### 3. Test Coverage Requirements
- **Minimum Coverage**: 80% for all new code
- **Critical Path Coverage**: 100% for:
  - Authentication/Authorization
  - Payment processing
  - Data generation
  - API endpoints
  - Security features

---

## Repository-Specific Testing Requirements

### inferloop-marketplace
```bash
# Required test suites
npm test                    # Unit tests
npm run test:integration    # Integration tests
npm run test:e2e           # End-to-end tests
npm run test:security      # Security tests
```

**Critical Test Areas**:
- [ ] Agent marketplace functionality
- [ ] Shopping cart operations
- [ ] User authentication
- [ ] Industry vertical filtering
- [ ] Payment processing
- [ ] Agent deployment workflow

### inferloop-datamint
```bash
# Required test suites
pytest tests/              # Unit tests
pytest tests/integration/  # Integration tests
pytest tests/generation/   # Data generation tests
```

**Critical Test Areas**:
- [ ] All generation methods (Faker, SDV, CTGAN, etc.)
- [ ] Schema validation
- [ ] Data quality metrics
- [ ] File upload/download
- [ ] Workflow management
- [ ] API endpoints

### inferloop-agentcraft
```bash
# Required test suites
npm test                   # Component tests
npm run test:agents        # Agent creation tests
npm run test:deployment    # Deployment tests
```

**Critical Test Areas**:
- [ ] Agent builder functionality
- [ ] Template system
- [ ] Component integration
- [ ] Agent validation
- [ ] Deployment pipeline

### inferloop-testnest
```bash
# Required test suites
npm test                   # Core tests
npm run test:validation    # Validation tests
npm run test:compliance    # Compliance tests
```

**Critical Test Areas**:
- [ ] Test execution engine
- [ ] Result reporting
- [ ] Performance benchmarks
- [ ] Security scanning
- [ ] Compliance checks

### inferloop-trustscan
```bash
# Required test suites
pytest tests/              # Security tests
pytest tests/scanning/     # Vulnerability scanning
pytest tests/compliance/   # Compliance validation
```

**Critical Test Areas**:
- [ ] Security scanning
- [ ] Vulnerability detection
- [ ] Compliance validation
- [ ] Audit logging
- [ ] Report generation

### inferloop-datalake
```bash
# Required test suites
npm test                   # Storage tests
npm run test:retrieval     # Data retrieval tests
npm run test:processing    # Processing pipeline tests
```

**Critical Test Areas**:
- [ ] Data storage operations
- [ ] Query performance
- [ ] Data integrity
- [ ] Backup/restore
- [ ] Access control

### inferloop-designs
```bash
# Required test suites
npm test                   # UI component tests
npm run test:visual        # Visual regression tests
npm run test:accessibility # Accessibility tests
```

**Critical Test Areas**:
- [ ] Component rendering
- [ ] User interactions
- [ ] Responsive design
- [ ] Accessibility compliance
- [ ] Theme consistency

### inferloop-agentforge
```bash
# Required test suites
npm test                   # Core tests
npm run test:forge         # Agent forging tests
npm run test:optimization  # Optimization tests
```

**Critical Test Areas**:
- [ ] Agent optimization
- [ ] Performance tuning
- [ ] Resource management
- [ ] Scaling tests
- [ ] Integration tests

---

## Test Categories

### 1. Unit Tests
- Test individual functions/methods
- Mock external dependencies
- Fast execution (<100ms per test)
- Run on every file save

### 2. Integration Tests
- Test component interactions
- Use test databases
- Test API endpoints
- Run before commits

### 3. End-to-End Tests
- Test complete user workflows
- Use production-like environment
- Test cross-service communication
- Run before deployments

### 4. Performance Tests
- Load testing
- Stress testing
- Memory leak detection
- Response time validation

### 5. Security Tests
- Vulnerability scanning
- Penetration testing
- Authentication testing
- Authorization testing

---

## Test Implementation Checklist

For EVERY change, ensure:

### Before Starting
- [ ] Identify affected components
- [ ] Review existing tests
- [ ] Plan new test cases
- [ ] Set up test data

### During Development
- [ ] Write unit tests first
- [ ] Implement feature/fix
- [ ] Add integration tests
- [ ] Update documentation

### Before Committing
- [ ] Run all test suites
- [ ] Check test coverage
- [ ] Fix any failing tests
- [ ] Review test output

### Before Merging
- [ ] Pass CI/CD pipeline
- [ ] Peer review tests
- [ ] Verify no regressions
- [ ] Update test documentation

---

## Regression Testing Protocol

### Daily Regression Suite
Run automatically at 2 AM UTC:
```bash
./scripts/run-regression-tests.sh
```

### Pre-Release Testing
Before any release:
1. Full regression test suite
2. Cross-browser testing
3. Load testing
4. Security scanning
5. Manual smoke tests

### Post-Deployment Verification
After deployment:
1. Health check endpoints
2. Critical path validation
3. Performance monitoring
4. Error rate monitoring

---

## Test Data Management

### Test Data Requirements
- Use synthetic data only
- No production data in tests
- Deterministic test data
- Isolated test environments

### DataMint Integration
Use DataMint for generating test data:
```python
from datamint import generate_test_data

test_data = generate_test_data(
    schema="customer",
    rows=100,
    method="faker"
)
```

---

## Continuous Integration Requirements

### GitHub Actions Workflow
```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests
        run: |
          npm test
          npm run test:coverage
      - name: Check Coverage
        run: |
          if [ $(npm run coverage:check) -lt 80 ]; then
            echo "Coverage below 80%"
            exit 1
          fi
```

### Pre-commit Hooks
```bash
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: run-tests
        name: Run Tests
        entry: npm test
        language: system
        pass_filenames: false
```

---

## Monitoring and Alerts

### Test Failure Alerts
- Immediate Slack notification
- Email to development team
- Block deployments
- Create incident ticket

### Coverage Monitoring
- Daily coverage reports
- Trend analysis
- Alert on coverage drop
- Monthly coverage review

---

## Enforcement

### Automated Enforcement
- Pre-commit hooks block commits without tests
- CI/CD pipeline fails without 80% coverage
- Deployments blocked if tests fail
- Automated rollback on test failures

### Manual Review
- Code reviews must verify test presence
- Test quality assessment
- Coverage verification
- Regression test confirmation

---

## Test Documentation

### Required Documentation
For each test:
- Purpose and scope
- Test data requirements
- Expected outcomes
- Edge cases covered
- Performance expectations

### Test Naming Convention
```javascript
// Good test names
test('should generate 100 rows of customer data using faker method')
test('should return 404 when agent ID does not exist')
test('should validate email format in user registration')

// Bad test names
test('test1')
test('works')
test('data generation')
```

---

## Exceptions

**There are NO exceptions to this policy.**

Even for:
- "Simple" changes
- "Urgent" fixes
- "Temporary" solutions
- "Documentation" updates
- "Configuration" changes

---

## Support and Resources

### Testing Tools
- **JavaScript/TypeScript**: Jest, Cypress, Playwright
- **Python**: pytest, unittest, nose2
- **API Testing**: Postman, RestAssured, SuperTest
- **Load Testing**: K6, JMeter, Locust
- **Security Testing**: OWASP ZAP, Burp Suite

### Training Resources
- Internal testing workshops (monthly)
- Testing best practices documentation
- Pair programming sessions
- Code review feedback

---

## Compliance

This policy is mandatory and will be enforced through:
1. Automated tooling
2. Code review process
3. Performance reviews
4. Deployment gates

**Non-compliance will result in:**
- Blocked pull requests
- Blocked deployments
- Required remediation
- Additional training requirements

---

## Review and Updates

This policy will be reviewed quarterly and updated based on:
- Incident analysis
- Team feedback
- Industry best practices
- Tool improvements

---

## Signature

By contributing to any Inferloop repository, you acknowledge and agree to follow this testing policy.

**Last Updated**: September 3, 2025  
**Next Review**: December 3, 2025

---

## Quick Reference Commands

```bash
# Run all tests for a repository
./scripts/test-all.sh

# Run specific test suite
npm test -- --suite=integration

# Generate coverage report
npm run test:coverage

# Run regression tests
./scripts/regression-test.sh

# Validate test compliance
./scripts/validate-tests.sh
```

---

**Remember: Every line of code without a test is a potential bug waiting to happen.**