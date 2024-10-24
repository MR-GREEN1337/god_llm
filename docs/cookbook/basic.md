# God Module Cookbook - Basic Examples

A collection of practical examples showing common use patterns of the God Module.

## 1. Simple Question Exploration

```python
from god_llm.core import God
from god_llm.plugins.groq import ChatGroq

# Initialize
god = God(llm=ChatGroq(api_key="you_api_key", model_name="model_name"))

# Basic exploration
node_id = god.expand("What are the implications of quantum computing?")

# Get paths
paths = god.pray(k=3)

# Print summaries
for path in god.miracle(k=3)["paths"]:
    print(f"Path score: {path['score']}")
    print(f"Summary: {path['summary']}\n")
```

## 2. Connected Reasoning Chains

```python
# Start with a root question
root_id = god.expand("What are the environmental impacts of AI?")

# Follow up on power consumption
energy_id = god.expand(
    "How does AI training affect energy consumption?",
    parent_id=root_id
)

# Explore solutions
solutions_id = god.expand(
    "What are potential solutions for reducing AI's energy footprint?",
    parent_id=energy_id
)

# Get the complete reasoning chain
paths = god.pray(k=1)
```

## 3. Comparative Analysis

```python
def compare_topics(god: God, topic1: str, topic2: str):
    # Analyze first topic
    id1 = god.expand(f"Analyze {topic1}")
    
    # Analyze second topic
    id2 = god.expand(f"Analyze {topic2}")
    
    # Compare both
    comparison_id = god.expand(
        f"Compare and contrast {topic1} and {topic2}",
        parent_id=id1  # Connect to first topic
    )
    
    # Get insights
    return god.miracle(k=1)

# Usage
results = compare_topics(
    god,
    "renewable energy",
    "nuclear power"
)
```

## 4. Deep Dive Analysis

```python
def deep_dive(god: God, topic: str, depth: int = 3):
    # Initial exploration
    current_id = god.expand(topic)
    
    # Deeper levels
    for level in range(depth):
        # Get current paths
        paths = god.pray(k=1)
        
        # Find most interesting question
        current_path = paths["paths"][0]
        next_question = current_path["questions"][0]
        
        # Explore further
        current_id = god.expand(
            next_question,
            parent_id=current_id
        )
    
    return god.miracle(k=1)

# Usage
analysis = deep_dive(
    god,
    "How does artificial intelligence impact privacy?",
    depth=3
)
```

## 5. Topic Mapping

```python
def map_related_topics(god: God, central_topic: str, num_branches: int = 3):
    # Central node
    center_id = god.expand(central_topic)
    
    # Create branches
    branch_ids = []
    for _ in range(num_branches):
        # Get current state
        paths = god.pray(k=1)
        
        # Pick a question
        question = paths["paths"][0]["questions"][0]
        
        # Create branch
        branch_id = god.expand(
            question,
            parent_id=center_id
        )
        branch_ids.append(branch_id)
    
    return god.miracle(k=num_branches)

# Usage
topic_map = map_related_topics(
    god,
    "What is machine learning?",
    num_branches=3
)
```

## 6. Iterative Refinement

```python
def refine_analysis(god: God, topic: str, iterations: int = 3):
    current_id = god.expand(topic)
    
    for i in range(iterations):
        # Get current insights
        paths = god.pray(k=1)
        
        # Generate refinement prompt
        refinement = f"Refine and expand on: {paths['paths'][0]['summary']}"
        
        # Create refined analysis
        current_id = god.expand(
            refinement,
            parent_id=current_id
        )
    
    return god.miracle(k=1)

# Usage
refined_analysis = refine_analysis(
    god,
    "What are the ethical implications of AI?",
    iterations=3
)
```

## 7. Batch Processing

```python
def batch_analyze(god: God, topics: List[str], max_nodes_per_topic: int = 5):
    results = {}
    
    for topic in topics:
        # Analyze with node limit
        node_id = god.expand(
            topic,
            max_nodes=max_nodes_per_topic
        )
        
        # Get summary
        summary = god.miracle(k=1)
        results[topic] = summary
    
    return results

# Usage
topics = [
    "Climate change solutions",
    "Future of transportation",
    "Space exploration"
]

batch_results = batch_analyze(god, topics)
```

## 8. Error Handling

```python
def safe_expansion(god: God, prompt: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            node_id = god.expand(
                prompt,
                retry_count=attempt
            )
            return node_id
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Retry {attempt + 1}/{max_retries}: {str(e)}")
    
    return None

# Usage
try:
    node_id = safe_expansion(
        god,
        "Complex analysis prompt"
    )
except Exception as e:
    print(f"Analysis failed: {str(e)}")
```