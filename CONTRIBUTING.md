# Contributing to Patent Expiration API

Thank you for your interest in contributing to the Patent Expiration API! 🎉

This document provides guidelines for contributing to this project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

---

## 📜 Code of Conduct

This project follows a Code of Conduct. By participating, you are expected to uphold this code:

- **Be respectful** and inclusive
- **Be collaborative** and helpful
- **Be professional** in all communications
- **Focus on what is best** for the community
- **Show empathy** towards other community members

---

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
```bash
   git clone https://github.com/YOUR_USERNAME/PatentExpirationAPI.git
   cd PatentExpirationAPI
```
3. **Add upstream remote:**
```bash
   git remote add upstream https://github.com/JovSele/PatentExpirationAPI.git
```

---

## 💻 Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Git
- Virtual environment tool

### Setup Steps
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your credentials
nano .env

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

### Get API Keys

1. **EPO OPS:** https://developers.epo.org/
2. **USPTO PatentsView:** https://search.patentsview.org/

---

## 🤝 How to Contribute

### Types of Contributions

We welcome:

- 🐛 **Bug fixes**
- ✨ **New features**
- 📝 **Documentation improvements**
- 🧪 **Tests**
- 🎨 **UI/UX improvements**
- 🌍 **Translations**
- 💡 **Ideas and suggestions**

### Before Starting

1. **Check existing issues** - someone might already be working on it
2. **Open an issue** to discuss major changes before implementation
3. **Keep PRs focused** - one feature/fix per PR

---

## 📏 Coding Standards

### Python Style Guide

We follow **PEP 8** with these tools:
```bash
# Format code
black app/ tests/

# Check linting
flake8 app/ tests/

# Type checking
mypy app/
```

### Code Structure

- **Keep functions small** (<50 lines)
- **Use type hints** for all function signatures
- **Write docstrings** for public functions
- **Follow existing patterns** in the codebase

### Example Function
```python
async def get_patent_status(patent_number: str) -> Optional[Dict[str, Any]]:
    """
    Fetch patent status from multiple sources.
    
    Args:
        patent_number: Patent identifier (e.g., "EP1234567")
        
    Returns:
        Patent data dict or None if not found
        
    Raises:
        InvalidPatentFormatException: If patent format is invalid
        PatentNotFoundException: If patent not found in any source
    """
    # Implementation
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: Add batch patent lookup endpoint
fix: Correct EPO OAuth token refresh
docs: Update API usage examples
test: Add tests for USPTO service
refactor: Simplify cache logic
chore: Update dependencies
```

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `style`: Code style (formatting)
- `chore`: Maintenance
- `perf`: Performance improvement

---

## 🧪 Testing

### Run Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=app tests/

# Specific test file
pytest tests/test_endpoints.py

# Specific test
pytest tests/test_endpoints.py::test_get_patent_status
```

### Writing Tests
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_patent_status_success():
    """Test successful patent lookup."""
    response = client.get("/api/v1/status?patent=EP1234567")
    assert response.status_code == 200
    assert response.json()["patent_number"] == "EP1234567"

def test_invalid_patent_format():
    """Test invalid patent format handling."""
    response = client.get("/api/v1/status?patent=INVALID")
    assert response.status_code == 400
```

### Test Coverage

- Aim for **>80% coverage**
- Test **happy paths** and **edge cases**
- Test **error handling**
- Mock external API calls

---

## 🔄 Pull Request Process

### 1. Create a Branch
```bash
git checkout -b feat/add-batch-lookup
```

Branch naming:
- `feat/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/what-changed` - Documentation
- `test/what-tested` - Tests

### 2. Make Changes

- Write clean, documented code
- Add tests for new functionality
- Update documentation if needed

### 3. Commit Changes
```bash
git add .
git commit -m "feat: Add batch patent lookup endpoint"
```

### 4. Push to Your Fork
```bash
git push origin feat/add-batch-lookup
```

### 5. Open Pull Request

- Go to GitHub and click "New Pull Request"
- Fill in the PR template
- Link related issues
- Request review

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Breaking change

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing done

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

### Review Process

1. **Automated checks** must pass (tests, linting)
2. **Code review** by maintainers
3. **Address feedback** and update PR
4. **Approval** and merge by maintainers

---

## 🐛 Issue Reporting

### Before Creating an Issue

1. **Search existing issues** - avoid duplicates
2. **Check documentation** - might be answered there
3. **Try latest version** - issue might be fixed

### Bug Report Template
```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Call endpoint '....'
3. See error

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11.5]
- API Version: [e.g., 1.0.0]

**Additional context**
Any other relevant information
```

### Feature Request Template
```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution**
How should it work?

**Alternatives considered**
Other approaches you've thought about

**Additional context**
Use cases, examples, mockups
```

---

## 📚 Resources

- **Documentation:** [README.md](README.md)
- **API Docs:** http://localhost:8000/docs
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **License:** [LICENSE](LICENSE)

### Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [pytest](https://docs.pytest.org/)

---

## 🏆 Recognition

Contributors will be:
- Listed in [CHANGELOG.md](CHANGELOG.md)
- Mentioned in release notes
- Added to contributors list

---

## 💬 Questions?

- **GitHub Issues:** For bugs and features
- **GitHub Discussions:** For questions and ideas
- **Email:** jovsele@gmail.com

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🙏**

Every contribution, no matter how small, is valuable and appreciated.