# Nodes Documentation

## Overview
The Node system forms the fundamental data structure of the God LLM framework. Each node represents a thought or response in the reasoning chain, maintaining relationships and context with other nodes.

## Node Class Structure

### Core Attributes
```python
@dataclass
class Node:
    prompt: Union[UserMessage, AIMessage]
    thought: AIMessage
    parent_id: Optional[str] = None
    context_history: List[Context] = field(default_factory=list)
    children: List[str] = field(default_factory=list)
    relations: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()))
    score: float = 1.0
```

### Context Class
```python
@dataclass
class Context:
    prompt: str
    thought: str
    depth: int
    node_id: str
```

## Node Relationships

### Hierarchical Relationships
1. **Parent-Child**
   - Each node has one optional parent
   - Nodes can have multiple children
   - Forms tree-like structure

2. **Context History**
   - Maintains list of ancestor contexts
   - Includes prompts and thoughts
   - Records depth information

3. **Lateral Relationships**
   - Based on semantic similarity
   - Bidirectional connections
   - Cross-branch relationships

## Node Operations

### Creation
```python
# Basic node creation
node = Node(
    prompt=UserMessage(content="What is consciousness?"),
    thought=AIMessage(content="Consciousness is..."),
)

# With context
node = Node(
    prompt=prompt_msg,
    thought=thought_msg,
    context_history=context_list,
    parent_id=parent_node_id
)
```

### Relationship Management
```python
# Add child
parent_node.children.append(child_node.id)

# Add relation
node1.relations.append(node2.id)
node2.relations.append(node1.id)
```

### Context Building
```python
# Build context history
contexts = []
current_id = node_id
while current_id and len(contexts) < max_depth:
    node = nodes[current_id]
    contexts.append(Context(
        prompt=node.prompt.content,
        thought=node.thought.content,
        depth=len(contexts),
        node_id=node.id
    ))
    current_id = node.parent_id
```

## Node Scoring

### Base Score
- Initial score of 1.0
- Modified based on various factors
- Used in path evaluation

### Context Retention Score
```python
def _compute_context_retention_score(self) -> float:
    if not self.context_history:
        return 1.0
    
    # Compute based on context utilization
    context_scores = []
    for ctx in self.context_history:
        relevance = compute_relevance(ctx, self.thought)
        context_scores.append(relevance)
    
    return np.mean(context_scores)
```

## Best Practices

1. **Node Creation**
   - Include comprehensive context
   - Set appropriate relationships
   - Validate inputs

2. **Relationship Management**
   - Maintain bidirectional relations
   - Update parent-child links
   - Clean up orphaned nodes

3. **Context Handling**
   - Limit context history depth
   - Include relevant context only
   - Maintain context order

## Implementation Examples

### Basic Node Usage
```python
# Create root node
root = Node(
    prompt=UserMessage("Initial question"),
    thought=AIMessage("Initial response")
)

# Add child node
child = Node(
    prompt=UserMessage("Follow-up question"),
    thought=AIMessage("Follow-up response"),
    parent_id=root.id,
    context_history=[Context(
        prompt=root.prompt.content,
        thought=root.thought.content,
        depth=0,
        node_id=root.id
    )]
)

# Set relationships
root.children.append(child.id)
```

### Context Management
```python
def build_context(node: Node, max_depth: int = 3) -> List[Context]:
    contexts = []
    current = node
    depth = 0
    
    while current.parent_id and depth < max_depth:
        parent = nodes[current.parent_id]
        contexts.append(Context(
            prompt=parent.prompt.content,
            thought=parent.thought.content,
            depth=depth,
            node_id=parent.id
        ))
        current = parent
        depth += 1
        
    return list(reversed(contexts))
```

### Relationship Building
```python
def build_relations(node: Node, nodes: Dict[str, Node], threshold: float = 0.7):
    for other_id, other_node in nodes.items():
        if other_id != node.id:
            similarity = compute_similarity(node, other_node)
            if similarity > threshold:
                node.relations.append(other_id)
                other_node.relations.append(node.id)
```

## Error Handling

1. **Node Validation**
   ```python
   def validate_node(node: Node) -> bool:
       if not node.prompt or not node.thought:
           return False
       if node.parent_id and node.parent_id not in nodes:
           return False
       return True
   ```

2. **Relationship Cleanup**
   ```python
   def cleanup_relations(nodes: Dict[str, Node]):
       for node in nodes.values():
           node.relations = [r for r in node.relations if r in nodes]
   ```

3. **Context Validation**
   ```python
   def validate_context(context: List[Context]) -> bool:
       if not context:
           return True
       depths = [ctx.depth for ctx in context]
       return depths == sorted(depths)
   ```

## Performance Considerations

1. **Memory Management**
   - Implement node cleanup strategies
   - Limit context history size
   - Monitor relationship growth

2. **Computation Efficiency**
   - Cache similarity calculations
   - Batch relationship updates
   - Optimize context building

3. **Storage Optimization**
   - Implement node serialization
   - Manage context history size
   - Clean up unused relationships