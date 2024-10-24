# Contributing Guide

Thank you for considering contributing to the God Module! This guide will help you get started with development contributions.

## Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mr-green1337/god_llm.git
cd god_llm
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Unix
# or
.\venv\Scripts\activate  # Windows

# Install development dependencies
pip install -e ".[dev]"
```

### 3. Install Pre-commit Hooks
```bash
pre-commit install
```

## Code Standards

### Style Guide
- Follow PEP 8 guidelines
- Use type hints for all functions
- Maximum line length: 88 characters (Black formatter)
- Docstring format: Google style

```python
def example_function(param1: str, param2: int) -> bool:
    """Does something useful with the parameters.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this error occurs
    """
    pass
```

### Testing
- Write unit tests for all new features
- Maintain minimum 90% test coverage
- Place tests in `tests/` directory

```python
# tests/test_example.py
import pytest
from god_llm.core import God

def test_expansion():
    god = God(llm=MockLLM())
    result = god.expand("test prompt")
    assert isinstance(result, str)
    assert len(result) > 0
```

## Pull Request Process

1. **Fork and Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-fix-name
   ```

2. **Commit Messages**
   ```bash
   # Format:
   # type(scope): description
   
   git commit -m "feat(core): add new expansion algorithm"
   git commit -m "fix(templates): correct prompt formatting"
   ```

3. **Testing**
   ```bash
   # Run tests
   pytest
   
   # Check coverage
   pytest --cov=god_llm tests/
   ```

4. **Documentation**
   - Update relevant documentation
   - Add docstrings for new functions
   - Include example usage

## Development Guidelines

### Adding New Features

1. **New LLM Provider**
```python
from god_llm.llm import BaseLLM

class NewLLMProvider(BaseLLM):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        # Implementation
        pass

    def get_embedding(self, text: str) -> List[float]:
        # Implementation
        pass
```

2. **New Template**
```python
from god_llm.templates import TemplateManager

def add_custom_template(template_manager: TemplateManager):
    template_manager.add_template(
        "new_template",
        "Custom prompt format: {variable}"
    )
```

3. **New Scoring Method**
```python
from god_llm.scoring import BaseScorer

class CustomScorer(BaseScorer):
    def compute_score(self, text: str) -> float:
        # Implementation
        pass
```

### Error Handling

```python
from god_llm.exceptions import GodError

class CustomError(GodError):
    """Custom error for specific cases."""
    pass

def example_function():
    try:
        # Implementation
        pass
    except Exception as e:
        raise CustomError(f"Meaningful error message: {str(e)}")
```

## Release Process

1. **Version Bump**
   ```bash
   # Update version in setup.py
   # Update CHANGELOG.md
   git commit -m "chore: bump version to X.Y.Z"
   ```

2. **Create Release**
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```

3. **Build and Upload**
   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

## Getting Help

- Open an issue for bugs
- Use discussions for questions
- Join our Discord community