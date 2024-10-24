# God Module Documentation

## Overview
The God module represents the core orchestrator of the contextual reasoning system. Named with inspiration from Proverbs 2:6, it manages the generation, evaluation, and exploration of knowledge paths using Large Language Models.

## Class: God

### Constructor Parameters

```python
def __init__(
    llm: BaseLLM,
    similarity_threshold: float = 0.7,
    max_iterations: int = 4,
    context_window: int = 3,
    min_question_score: MinQuestionScore = MinQuestionScore(min_question_score=0.4),
    template_manager: Optional[TemplateManager] = None,
    debug: bool = False
)
```

- `llm`: Base language model interface
- `similarity_threshold`: Threshold for node relationships (0.0-1.0)
- `max_iterations`: Maximum depth of reasoning chains
- `context_window`: Number of previous nodes to maintain in context
- `min_question_score`: Minimum score for generated questions
- `template_manager`: Manager for prompt templates
- `debug`: Enable detailed logging

### Core Methods

#### expand()
```python
def expand(
    prompt: str, 
    parent_id: Optional[str] = None, 
    depth: int = 0, 
    retry_count: int = 0, 
    max_nodes: int = 15
) -> str
```

Expands a prompt into a thought and generates follow-up questions:
- Creates new node with response to prompt
- Generates and filters follow-up questions
- Builds relationships with existing nodes
- Implements retry logic for irrelevant responses
- Returns node ID of created node

#### pray()
```python
def pray(k: int = 3) -> Dict[str, List[Dict]]
```

Discovers and evaluates knowledge paths:
- Finds all possible paths through nodes
- Computes comprehensive path scores
- Returns top-k paths for each root node
- Includes detailed metrics and trajectory information

#### miracle()
```python
def miracle(k: int = 3) -> Dict[str, List[Dict]]
```

Generates human-readable summaries of best paths:
- Builds on pray() operation
- Creates natural language summaries
- Includes scores and metrics
- Returns structured results dictionary

### Internal Methods

#### Context Management
- `_build_context_history()`: Builds context from previous nodes
- `_create_enhanced_prompt()`: Enhances prompts with context
- `_find_relations()`: Discovers node relationships

#### Quality Control
- `_is_node_relevant()`: Evaluates node relevance
- `_generate_and_filter_questions()`: Creates and filters questions
- `_delete_node()`: Removes irrelevant nodes

#### Path Analysis
- `_find_paths()`: Discovers all possible paths
- `_compute_path_score()`: Evaluates path quality
- Various metric computation methods

## Usage Examples

### Basic Usage
```python
from god_llm.core import God
from my_llm_implementation import MyLLM

# Initialize
god = God(llm=MyLLM())

# Generate initial response
node_id = god.expand("What is the nature of consciousness?")

# Get top reasoning paths
paths = god.pray(k=3)

# Generate readable summaries
summaries = god.miracle(k=3)
```

### With Debug Logging
```python
god = God(
    llm=MyLLM(),
    debug=True,
    similarity_threshold=0.8,
    max_iterations=5
)
```

### Custom Template Manager
```python
from god_llm.templates import TemplateManager

templates = TemplateManager()
templates.add_template("custom_prompt", "...")

god = God(llm=MyLLM(), template_manager=templates)
```

## Best Practices

1. **Configuration**
   - Adjust `similarity_threshold` based on desired relationship strictness
   - Set `max_iterations` based on needed exploration depth
   - Configure `context_window` based on memory requirements

2. **Performance**
   - Monitor node count with `max_nodes` parameter
   - Enable debug logging for troubleshooting
   - Use appropriate batch sizes for operations

3. **Quality Control**
   - Implement retry logic for failed generations
   - Monitor and handle irrelevant nodes
   - Validate generated questions

## Error Handling

The God class implements various error handling mechanisms:
- Retry logic for failed expansions
- Node relevance checking
- Question quality filtering
- Context validation

## Limitations

1. Memory Usage
   - Node count grows with exploration depth
   - Context history affects memory consumption
   - Large paths can impact performance

2. Performance
   - Path finding complexity grows with node count
   - Multiple LLM calls per expansion
   - Similarity computations can be intensive

3. Quality Control
   - Depends on LLM quality
   - Requires careful threshold tuning
   - May need domain-specific adjustments

## Implementation Tips

1. Monitor system resources:
   ```python
   god = God(debug=True)
   god.expand("prompt", max_nodes=20)  # Limit node count
   ```

2. Implement cleanup strategies:
   ```python
   # Regular cleanup of old nodes
   for node_id in list(god.nodes.keys()):
       if god.nodes[node_id].age > max_age:
           god._delete_node(node_id)
   ```

3. Use batch processing for large operations:
   ```python
   # Process in batches
   results = []
   for batch in chunks(prompts, batch_size):
       results.extend(god.expand(prompt) for prompt in batch)
   ```