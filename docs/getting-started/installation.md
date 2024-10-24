# Installation

## Quick Start

You can install god_llm directly from PyPI:

```bash
pip install god_llm
```

## Prerequisites

Before installing god_llm, ensure you have:
- Python 3.8 or higher
- pip (Python package installer)
- A compatible LLM API key (e.g., Groq, OpenAI, Anthropic)

## Installation Methods

### From PyPI (Recommended)

The simplest way to install god_llm is through PyPI:

```bash
pip install god_llm
```

### From Source

For the latest development version:

```bash
git clone https://github.com/MR-GREEN1337/god_llm.git
cd god_llm
pip install -e .
```

### Development Installation

If you plan to contribute to god_llm, install with development dependencies:

```bash
pip install -e ".[dev]"
```

## LLM Provider Setup

god_llm supports multiple LLM providers. Here's how to set up each one:

### Groq

1. Get your API key from [Groq's platform](https://console.groq.com)
2. Set up your environment:
   ```bash
   export GROQ_API_KEY="your-api-key-here"
   ```

### Installing Optional Dependencies

For additional features, install the relevant extras:

```bash
# For visualization support
pip install "god_llm[viz]"

# For all optional features
pip install "god_llm[all]"
```

## Verification

Verify your installation:

```python
from god_llm.core.god import God
from god_llm.plugins.groq import ChatGroq

# Initialize with Groq
llm = ChatGroq(
    model_name="llama-3.1-70b-versatile",
    api_key="your-api-key"  # Or use environment variable
)

# Create God instance
god = God(llm=llm)

# Test the installation
result = god.expand("What is the meaning of life?")
print("Installation successful!" if result else "Installation failed!")
```

## Common Issues

### API Key Not Found
```python
ApiKeyError: API key not found
```
**Solution:** Ensure you've properly set your API key either in the environment or when initializing the LLM.

### Dependency Conflicts
```python
ImportError: Cannot import name 'X' from 'Y'
```
**Solution:** Try creating a fresh virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install god_llm
```

## Overview

god_llm is a framework for recursive thought expansion using Large Language Models. It enables deep exploration of ideas while maintaining context and relevance. The package includes:

- Core functionality for thought expansion
- Multiple LLM provider integrations
- Visualization tools
- Advanced scoring and path finding

## Further Reading

- [Official Documentation](https://mr-green1337.github.io/god_llm/)
- [Let's Build a God LLM](https://medium.com/@islamhachimi/lets-a-build-a-god-llm-0beaf2460659) - Original concept article
- [Contributing Guidelines](https://github.com/MR-GREEN1337/god_llm/blob/main/CONTRIBUTING.md)
- [API Reference](https://mr-green1337.github.io/god_llm/api-reference/)