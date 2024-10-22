from dataclasses import dataclass
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
from uuid import uuid4
from god_llm.plugins.base import BaseMessage, UserMessage
from god_llm.utils.tfidf import TfidfVectorizer
import numpy as np

class Context(BaseModel):
    prompt: str
    thought: str
    depth: int
    node_id: str

class Node(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    parent_id: Optional[str] = None
    prompt: BaseMessage
    thought: BaseMessage
    children: List[str] = Field(default_factory=list)
    relations: List[str] = Field(default_factory=list)
    metadata: Optional[Dict] = None
    score: float = Field(default_factory=lambda: 0.0, ge=0.0, le=1.0)
    context_history: List[Context] = []
    vectorizer: TfidfVectorizer = Field(default_factory=lambda: TfidfVectorizer(max_features=384))

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like TfidfVectorizer

    @field_validator("score")
    def validate_score(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("Score must be between 0 and 1")
        return v

    @field_validator("parent_id")
    def validate_parent_id(cls, v):
        if isinstance(v, UserMessage):
            return None
        return v

    def __post_init__(self):
        self._compute_score()

    def _compute_score(self):
        # Prepare texts
        prompt_text = self.prompt.content
        thought_text = self.thought.content
        
        # Compute TF-IDF
        self.vectorizer.fit([prompt_text, thought_text])
        prompt_vec, thought_vec = self.vectorizer.transform([prompt_text, thought_text])
        
        # Calculate semantic similarity
        semantic_score = float(np.dot(prompt_vec, thought_vec) / 
                             (np.linalg.norm(prompt_vec) * np.linalg.norm(thought_vec)))
        
        # Length ratio penalty
        prompt_len = len(prompt_text.split())
        thought_len = len(thought_text.split())
        length_ratio = min(prompt_len, thought_len) / max(prompt_len, thought_len)
        
        # Context retention score
        context_score = self._compute_context_retention_score()
        
        depth_factor = 0.8 if self.parent_id else 1.0
        
        self.score = min(semantic_score * length_ratio * depth_factor * context_score, 1.0)
    
    def _compute_context_retention_score(self) -> float:
        if not self.context_history:
            return 1.0
            
        # Calculate similarity between current thought and all previous contexts
        thought_text = self.thought.content
        context_texts = [f"{ctx.prompt} {ctx.thought}" for ctx in self.context_history]
        
        if not context_texts:
            return 1.0
            
        # Fit vectorizer with all texts including current thought
        all_texts = context_texts + [thought_text]
        self.vectorizer.fit(all_texts)
        
        # Transform all texts
        vectors = self.vectorizer.transform(all_texts)
        thought_vector = vectors[-1]
        context_vectors = vectors[:-1]
        
        # Calculate similarities with decay factor
        similarities = []
        for i, context_vector in enumerate(context_vectors):
            similarity = float(np.dot(thought_vector, context_vector) / 
                            (np.linalg.norm(thought_vector) * np.linalg.norm(context_vector)))
            depth = self.context_history[i].depth
            decay_factor = np.exp(-0.3 * depth)  # Exponential decay based on depth
            similarities.append(similarity * decay_factor)
            
        return np.mean(similarities) if similarities else 1.0
