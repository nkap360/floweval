# Contributing to FlowEval API

Thank you for your interest in contributing to FlowEval! This guide will help you get started with contributing code, documentation, or other improvements to our REST API.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Documentation](#documentation)
- [Community](#community)

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

**Expected Behavior:**
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards others

**Unacceptable Behavior:**
- Harassment of any kind
- Trolling or insulting comments
- Publishing private information
- Other unprofessional conduct

---

## 🚀 Getting Started

### Prerequisites

**Development Requirements:**
```bash
Python >= 3.9
pip >= 21.0
Docker >= 20.0.0 (optional, for containerized development)
```

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

```bash
git clone https://github.com/YOUR_USERNAME/floweval.git
cd floweval
```

3. **Add upstream remote**:

```bash
git remote add upstream https://github.com/nkap360/floweval.git
```

### Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### Development Environment

1. **Copy environment template**:

```bash
cp .env.example .env
```

2. **Add your API keys** to `.env` file
3. **Start the API server**:

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access the API**:
- API Base URL: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

## 🔄 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

**Branch Naming Conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or changes
- `chore/` - Maintenance tasks

### 2. Make Your Changes

- Write clean, readable code
- Follow project conventions
- Add tests for new features
- Update documentation as needed

### 3. Test Your Changes

**Run All Tests:**
```bash
cd backend
pytest
pytest --cov=backend  # With coverage
flake8 .
mypy .
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add amazing feature"
```

See [Commit Guidelines](#commit-guidelines) below.

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

---

## 🎨 Code Style

### Python

**Style Guide:** PEP 8 + Black formatter

**Configuration:**
- Black for formatting (line length: 88)
- Flake8 for linting
- mypy for type checking
- isort for import sorting

**Key Conventions:**
```python
# ✅ DO: Use type hints
def process_dataset(dataset_id: str, config: Dict[str, Any]) -> DatasetResult:
    """Process a dataset with given configuration.
    
    Args:
        dataset_id: UUID of the dataset
        config: Configuration dictionary
        
    Returns:
        DatasetResult object with processing results
        
    Raises:
        ValueError: If dataset_id is invalid
    """
    # Implementation
    pass

# ✅ DO: Use descriptive names
def extract_questions_from_document(document: Document) -> List[Question]:
    pass

# ❌ DON'T: Use single-letter names (except for loops)
def process(d):
    pass

# ✅ DO: Use docstrings for all public functions
def calculate_score(items: List[Item]) -> float:
    """Calculate average score from list of items."""
    return sum(item.score for item in items) / len(items)

# ✅ DO: Use context managers
with open('file.txt', 'r') as f:
    content = f.read()

# ✅ DO: Use list comprehensions when appropriate
squares = [x**2 for x in range(10)]
```

**Running Tools:**
```bash
cd backend
black .              # Format code
flake8 .            # Lint code
mypy .              # Type check
isort .             # Sort imports
```

---

## 🧪 Testing

### API Testing

**Framework:** pytest

```python
# Example: Action handler test
import pytest
from backend.core.models import FlowNode
from backend.actions.actions_dataset import handle_load_dataset

@pytest.mark.asyncio
async def test_load_dataset_success():
    """Test successful dataset loading."""
    node = FlowNode(
        id="test-node",
        type="action",
        data={"actionId": "load_dataset", "params": {"dataset_id": "test-123"}}
    )
    
    result = await handle_load_dataset(node, {})
    
    assert result["status"] == "success"
    assert "dataset" in result
    assert result["dataset"]["id"] == "test-123"

@pytest.mark.asyncio
async def test_load_dataset_not_found():
    """Test dataset not found error."""
    node = FlowNode(
        id="test-node",
        type="action",
        data={"actionId": "load_dataset", "params": {"dataset_id": "nonexistent"}}
    )
    
    with pytest.raises(ValueError, match="Dataset not found"):
        await handle_load_dataset(node, {})
```

**Run Tests:**
```bash
cd backend
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest --cov=backend             # With coverage
pytest --cov-report=html         # HTML coverage report
pytest -k test_load_dataset      # Run specific tests
```

### Test Coverage Requirements

- **Minimum coverage:** 80% for new code
- **Critical paths:** 100% coverage for auth, data persistence
- **All new features** must include tests
- **Bug fixes** should include regression tests

---

## 📝 Commit Guidelines

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

**Scope (optional):**
- `api`: API changes
- `ui`: UI components
- `backend`: Backend changes
- `frontend`: Frontend changes
- `docs`: Documentation
- `test`: Tests

**Examples:**

```bash
feat(api): add dataset export endpoint

Add new POST /datasets/{id}/export endpoint that generates
downloadable JSON files. Includes format validation and error handling.

Closes #123

---

fix(ui): resolve PDF viewer memory leak

Fix memory leak in PDF viewer component by properly cleaning up
canvas references on unmount.

Fixes #456

---

docs: update installation guide

Add troubleshooting section for common Windows installation issues
and clarify Python version requirements.

---

refactor(backend): simplify flow executor logic

Extract node execution into separate methods for better testability
and maintainability. No functional changes.

---

test(api): add integration tests for dataset API

Add comprehensive test coverage for dataset CRUD operations
including edge cases and error scenarios.
```

### Commit Best Practices

✅ **DO:**
- Write clear, concise commit messages
- Commit early and often
- Keep commits atomic (one logical change per commit)
- Reference issues in commit messages

❌ **DON'T:**
- Mix unrelated changes in one commit
- Write vague messages like "fix bug" or "update code"
- Commit commented-out code
- Include sensitive information

---

## 🔀 Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] Branch is up to date with main
- [ ] No merge conflicts

**Update Your Branch:**
```bash
git fetch upstream
git rebase upstream/main
git push origin feature/your-feature --force-with-lease
```

### Creating the Pull Request

1. **Go to GitHub** and create a new pull request
2. **Fill out the template** completely
3. **Link related issues** using "Closes #123"
4. **Add screenshots** for UI changes
5. **Request reviewers**

**PR Title Format:**
```
feat: add dataset export feature (#123)
fix: resolve memory leak in PDF viewer (#456)
docs: update API documentation
```

### PR Description Template

```markdown
## Description
Brief description of changes made

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested? Include steps to reproduce

## Screenshots
(If applicable)

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented if necessary)

## Related Issues
Closes #123
Related to #456
```

### Review Process

1. **Automated checks** must pass (tests, linting, build)
2. **At least one approval** required from maintainers
3. **Address review comments** promptly
4. **Keep discussion professional** and constructive

**Responding to Feedback:**
```bash
# Make requested changes
git add .
git commit -m "refactor: address review comments"
git push origin feature/your-feature
```

### After Merge

1. **Delete your branch**:
```bash
git checkout main
git pull upstream main
git branch -d feature/your-feature
git push origin --delete feature/your-feature
```

2. **Update local main**:
```bash
git pull upstream main
```

---

## 📚 Documentation

### What to Document

**Always document:**
- New features and APIs
- Breaking changes
- Configuration changes
- Migration guides
- Troubleshooting steps

**Documentation Types:**
- **Code comments:** For complex logic
- **Docstrings:** For all public functions
- **README updates:** For new features
- **API docs:** For endpoint changes
- **User guides:** For UI changes

### Documentation Style

**Code Comments:**
```typescript
// ✅ GOOD: Explain WHY, not WHAT
// Use exponential backoff to avoid overwhelming the API during high load
await retryWithBackoff(apiCall, { maxRetries: 3 });

// ❌ BAD: States the obvious
// Retry the API call 3 times
await retryWithBackoff(apiCall, { maxRetries: 3 });
```

**Docstrings:**
```python
def generate_goldens(document: Document, count: int = 10) -> List[Golden]:
    """Generate question-answer pairs from document.
    
    Uses AI to analyze document content and create high-quality
    Q&A pairs suitable for evaluation datasets.
    
    Args:
        document: Source document to extract questions from
        count: Number of goldens to generate (default: 10)
        
    Returns:
        List of Golden objects with questions, answers, and context
        
    Raises:
        ValueError: If document is empty or invalid
        APIError: If AI provider fails
        
    Example:
        >>> doc = Document(content="...")
        >>> goldens = generate_goldens(doc, count=5)
        >>> print(len(goldens))
        5
    """
    pass
```

---

## 🌐 Community

### Communication Channels

- **GitHub Issues:** Bug reports and feature requests
- **GitHub Discussions:** Questions and community chat
- **Pull Requests:** Code review and collaboration

### Getting Help

**For Contributors:**
1. Check existing issues and discussions
2. Read documentation thoroughly
3. Ask in GitHub Discussions
4. Reach out to maintainers

**For Maintainers:**
- Respond to issues within 48 hours
- Review PRs within 1 week
- Be welcoming to new contributors
- Provide constructive feedback

### Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes
- Project README
- Special thanks in major releases

---

## 🏆 Contribution Areas

### Code Contributions

- New features
- Bug fixes
- Performance improvements
- Test coverage
- Code refactoring

### Non-Code Contributions

- Documentation improvements
- Tutorial creation
- Translation
- Issue triage
- Community support
- Design and UX feedback

### Beginner-Friendly

Look for issues tagged:
- `good-first-issue`
- `help-wanted`
- `documentation`
- `beginner-friendly`

---

## 📊 Release Process

### Version Numbers

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR:** Breaking changes
- **MINOR:** New features (backwards compatible)
- **PATCH:** Bug fixes

### Release Checklist

1. Update version in `package.json` and `backend/main.py`
2. Update CHANGELOG.md
3. Run full test suite
4. Create release tag
5. Build and publish artifacts
6. Update documentation
7. Announce release

---

## ✅ Final Checklist

Before submitting your contribution:

- [ ] Code follows style guidelines
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] PR description complete
- [ ] No merge conflicts
- [ ] Linked to related issues
- [ ] Screenshots included (if UI change)

---

## 🙏 Thank You!

Your contributions make Flow Builder better for everyone. We appreciate your time and effort!

**Questions?** Open a GitHub Discussion or reach out to maintainers.

---

**Last Updated:** December 3, 2025  
**Maintainer:** Flow Builder Team  
**License:** MIT
