# Scoring Documentation

## Overview
The scoring system in God LLM provides comprehensive evaluation of reasoning paths through multiple metrics. This sophisticated scoring approach ensures high-quality, coherent, and meaningful knowledge exploration.

## Scoring Metrics

### ScoreMetric Enum
```python
class ScoreMetric(Enum):
    DEPTH = "depth"
    RELATION = "relation"
    COHERENCE = "coherence"
    NOVELTY = "novelty"
    CONTEXT_RETENTION = "context_retention"
    HIERARCHY = "hierarchy"
```

### Metric Weights
```python
metric_weights = {
    ScoreMetric.DEPTH: 0.25,
    ScoreMetric.RELATION: 0.15,
    ScoreMetric.COHERENCE: 0.25,
    ScoreMetric.NOVELTY: 0.15,
    ScoreMetric.CONTEXT_RETENTION: 0.20,
    ScoreMetric.HIERARCHY: 0.20
}
```

## Scoring Components

### 1. Depth Score
Evaluates the depth and thoroughness of reasoning:
```python
def _compute_depth_score(self, path: List[str]) -> float:
    return np.mean([self.nodes[node_id].score for node_id in path])
```

### 2. Relation Score
Measures lateral connections between nodes:
```python
def _compute_relation_score(self, path: List[str]) -> float:
    if len(path) < 2:
        return 1.0
        
    relation_scores = []
    for node_id in path:
        node = self.nodes[node_id]
        related_nodes = set(node.relations).intersection(set(path))
        potential_relations = len(path) - 1
        score = len(related_nodes) / potential_relations if potential_relations > 0 else 0
        relation_scores.append(score)
        
    return np.mean(relation_scores)
```

### 3. Coherence Score
Evaluates logical flow and consistency:
```python
def _compute_coherence_score(self, path: List[str]) -> float:
    if len(path) < 2:
        return 1.0
        
    coherence_scores = []
    for i in range(len(path) - 1):
        current_node = self.nodes[path[i]]
        next_node = self.nodes[path[i + 1]]
        similarity = self._compute_similarity(current_node, next_node)
        coherence_scores.append(similarity)
        
    return np.mean(coherence_scores)
```

### 4. Novelty Score
Assesses uniqueness of insights:
```python
def _compute_novelty_score(self, path: List[str]) -> float:
    path_nodes = [self.nodes[node_id] for node_id in path]
    other_nodes = [node for node_id, node in self.nodes.items() 
                   if node_id not in path]
    
    if not other_nodes:
        return 0.5
        
    novelty_scores = []
    for path_node in path_nodes:
        similarities = [self._compute_similarity(path_node, other_node) 
                      for other_node in other_nodes]
        novelty_scores.append(1 - np.mean(similarities))
        
    return np.mean(novelty_scores)
```

### 5. Context Retention Score
Measures maintenance of context:
```python
def _compute_context_retention_score(self, path: List[str]) -> float:
    if len(path) < 2:
        return 1.0
        
    retention_scores = []
    for i in range(1, len(path)):
        current_node = self.nodes[path[i]]
        context_score = current_node._compute_context_retention_score()
        retention_scores.append(context_score)
        
    return np.mean(retention_scores)
```

### 6. Hierarchy Score
Evaluates strength of hierarchical relationships:
```python
def _compute_hierarchy_score(self, path: List[str]) -> float:
    if len(path) < 2:
        return 1.0
```
