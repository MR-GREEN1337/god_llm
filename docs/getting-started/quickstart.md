# Quickstart Guide

Get started with the God Module, a contextual reasoning system powered by Large Language Models.

## Installation

```bash
pip install god_llm
```

## Basic Usage

### 1. Initialize the God Module

```python
from god_llm.core import God
from god_llm.plugins.groq import ChatGroq

# Initialize with default settings
llm = ChatGroq(
    model_name="llama-3.1-70b-versatile",
    api_key="", #Dummy API key
)
god = God(llm=llm)
```

### 2. Generate Initial Thoughts

```python
# Create your first node
node_id = god.expand("What is the role of artificial intelligence in healthcare?")
```

### 3. Discover Reasoning Paths

```python
# Get top 3 reasoning paths
paths = god.pray(k=3)

# Generate human-readable summaries
summaries = god.miracle(k=3)
```

## Advanced Configuration

For more control over the system's behavior:

```python
god = God(
    llm=YourLLM(),
    similarity_threshold=0.8,  # Higher threshold for stricter relationships
    max_iterations=5,         # Deeper exploration
    context_window=4,         # Larger context history
    debug=True               # Enable detailed logging
)
```

## Common Use Cases

### 1. Sequential Reasoning

```python
# Start with an initial question
root_id = god.expand("What are the environmental impacts of renewable energy?")

# Explore a specific aspect
follow_up_id = god.expand("How does battery production affect sustainability?", parent_id=root_id)

# Get the reasoning chain
paths = god.pray(k=1)
```

### 2. Batch Processing

```python
questions = [
    "What are the ethical implications of AI?",
    "How does quantum computing affect cybersecurity?",
    "What role does blockchain play in finance?"
]

# Process multiple questions
node_ids = [god.expand(q, max_nodes=5) for q in questions]
```

### 3. Quality Control

```python
god = God(
    llm=YourLLM(),
    similarity_threshold=0.85  # Higher relevance requirement
)

# Expansion with retry logic
node_id = god.expand("Complex topic", retry_count=2)
```

## Best Practices

1. **Resource Management**
   - Set `max_nodes` limit for large explorations
   - Monitor system memory usage with debug mode
   - Use appropriate batch sizes for bulk operations

2. **Quality Optimization**
   - Adjust similarity threshold based on your needs
   - Configure minimum question scores for better relevance
   - Use context window size appropriate for your use case

3. **Error Handling**
   - Implement try-except blocks for expansions
   - Monitor debug logs for issues
   - Clean up old nodes regularly

## Performance Tips

```python
# Regular cleanup
def cleanup_old_nodes(god_instance, max_age):
    for node_id in list(god_instance.nodes.keys()):
        if god_instance.nodes[node_id].age > max_age:
            god_instance._delete_node(node_id)

# Batch processing with resource limits
def process_batch(god_instance, prompts, batch_size=5):
    results = []
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i + batch_size]
        results.extend(god_instance.expand(p, max_nodes=10) for p in batch)
    return results
```

## Next Steps

- Explore advanced features in the full documentation
- Customize prompt templates for your use case
- Implement domain-specific quality controls
- Monitor and optimize system performance