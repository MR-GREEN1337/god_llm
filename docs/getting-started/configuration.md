# Configuration Guide

Learn how to configure and customize the God Module for your specific needs.

## Basic Configuration

### Constructor Parameters

```python
from god_llm.core import God
from god_llm.templates import TemplateManager
from god_llm.scoring import MinQuestionScore

god = God(
    llm=YourLLM(),                    # Required: Language model interface
    similarity_threshold=0.7,          # Optional: Default 0.7
    max_iterations=4,                  # Optional: Default 4
    context_window=3,                  # Optional: Default 3
    min_question_score=MinQuestionScore(min_question_score=0.4),  # Optional
    template_manager=None,             # Optional: Custom template manager
    debug=False                        # Optional: Default False
)
```

## Parameter Details

### 1. Language Model (`llm`)
```python
# Example custom LLM implementation
from god_llm.llm import BaseLLM

class CustomLLM(BaseLLM):
    def generate(self, prompt: str) -> str:
        # Your implementation here
        pass

    def get_embedding(self, text: str) -> List[float]:
        # Your implementation here
        pass

god = God(llm=CustomLLM())
```

### 2. Similarity Threshold (`similarity_threshold`)
```python
# Higher threshold for stricter relationship matching
god = God(
    llm=YourLLM(),
    similarity_threshold=0.85  # Only very similar nodes will be connected
)

# Lower threshold for more flexible connections
god = God(
    llm=YourLLM(),
    similarity_threshold=0.6   # More nodes will be considered related
)
```

### 3. Maximum Iterations (`max_iterations`)
```python
# Deep exploration
god = God(
    llm=YourLLM(),
    max_iterations=6    # Allow deeper reasoning chains
)

# Shallow exploration
god = God(
    llm=YourLLM(),
    max_iterations=2    # Keep reasoning chains short
)
```

### 4. Context Window (`context_window`)
```python
# Large context window
god = God(
    llm=YourLLM(),
    context_window=5    # Keep more previous nodes in context
)

# Minimal context
god = God(
    llm=YourLLM(),
    context_window=1    # Only use immediate parent node
)
```

### 5. Minimum Question Score (`min_question_score`)
```python
# Strict question filtering
god = God(
    llm=YourLLM(),
    min_question_score=MinQuestionScore(min_question_score=0.7)  # Only high-quality questions
)

# Lenient question filtering
god = God(
    llm=YourLLM(),
    min_question_score=MinQuestionScore(min_question_score=0.3)  # Accept more questions
)
```

### 6. Template Manager (`template_manager`)
```python
# Custom templates
template_manager = TemplateManager()

# Add custom prompts
template_manager.add_template(
    "custom_expansion",
    "Given the context '{context}', analyze the following: {prompt}"
)

template_manager.add_template(
    "custom_question",
    "Generate relevant questions about: {topic}"
)

god = God(
    llm=YourLLM(),
    template_manager=template_manager
)
```

### 7. Debug Mode (`debug`)
```python
# Enable detailed logging
god = God(
    llm=YourLLM(),
    debug=True
)
```

## Configuration Profiles

### Deep Analysis Profile
```python
god = God(
    llm=YourLLM(),
    similarity_threshold=0.8,
    max_iterations=6,
    context_window=4,
    min_question_score=MinQuestionScore(min_question_score=0.6),
    debug=True
)
```

### Quick Exploration Profile
```python
god = God(
    llm=YourLLM(),
    similarity_threshold=0.6,
    max_iterations=2,
    context_window=1,
    min_question_score=MinQuestionScore(min_question_score=0.4),
    debug=False
)
```

### Memory-Optimized Profile
```python
god = God(
    llm=YourLLM(),
    similarity_threshold=0.7,
    max_iterations=3,
    context_window=2,
    min_question_score=MinQuestionScore(min_question_score=0.5),
    debug=False
)
```

## Runtime Configuration

### Expand Method Parameters
```python
# Configure individual expand operations
node_id = god.expand(
    prompt="Your prompt here",
    parent_id="optional_parent_id",    # Connect to specific node
    depth=0,                           # Starting depth
    retry_count=2,                     # Number of retries
    max_nodes=15                       # Node limit
)
```

### Path Analysis Configuration
```python
# Configure path analysis
paths = god.pray(k=3)          # Get top 3 paths
summaries = god.miracle(k=5)   # Get top 5 summarized paths
```

## Best Practices

### 1. Resource Management
```python
# For memory-intensive operations
god = God(
    llm=YourLLM(),
    context_window=2,          # Smaller context
    max_iterations=3,          # Limited depth
    debug=True                # Monitor resource usage
)
```

### 2. Quality Optimization
```python
# For high-quality results
god = God(
    llm=YourLLM(),
    similarity_threshold=0.85,
    min_question_score=MinQuestionScore(min_question_score=0.7),
    max_iterations=5
)
```

### 3. Performance Optimization
```python
# For faster processing
god = God(
    llm=YourLLM(),
    context_window=1,
    max_iterations=2,
    debug=False
)
```

## Troubleshooting

### Common Issues
1. High Memory Usage:
   - Reduce `context_window`
   - Lower `max_iterations`
   - Implement regular cleanup

2. Poor Quality Results:
   - Increase `similarity_threshold`
   - Raise `min_question_score`
   - Use custom templates

3. Slow Performance:
   - Reduce `max_iterations`
   - Lower `context_window`
   - Batch process with limits