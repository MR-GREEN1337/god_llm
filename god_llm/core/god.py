import os
import time
from typing import List, Optional, Dict, Set, Union, Tuple
import numpy as np
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict, deque
import heapq
from loguru import logger

from god_llm.templates.base import TemplateManager
from god_llm.plugins.base import AIMessage, BaseLLM, UserMessage
from god_llm.utils.tfidf import TfidfVectorizer
from .base import Node, Context

class ScoreMetric(Enum):
    DEPTH = "depth"
    RELATION = "relation"
    COHERENCE = "coherence"
    NOVELTY = "novelty"
    CONTEXT_RETENTION = "context_retention"

@dataclass
class PathScore:
    total: float
    metrics: Dict[ScoreMetric, float]

class God:
    def __init__(
        self,
        llm: BaseLLM,
        similarity_threshold: float = 0.7,
        max_iterations: int = 4,
        context_window: int = 3,
        template_manager: Optional[TemplateManager] = None,
        debug: bool = False,
    ):
        self.debug = debug
        if self.debug:
            logger.add("god_llm.log", rotation="10 MB", level="INFO")
            logger.info(f"Initializing EnhancedGod with parameters: "
                       f"similarity_threshold={similarity_threshold}, "
                       f"max_iterations={max_iterations}, "
                       f"context_window={context_window}")
            
        self.llm = llm
        self.similarity_threshold = similarity_threshold
        self.max_iterations = max_iterations
        self.context_window = context_window
        self.template_manager = template_manager or TemplateManager()
        self.nodes: Dict[str, Node] = {}
        
        self.metric_weights = {
            ScoreMetric.DEPTH: 0.25,
            ScoreMetric.RELATION: 0.15,
            ScoreMetric.COHERENCE: 0.25,
            ScoreMetric.NOVELTY: 0.15,
            ScoreMetric.CONTEXT_RETENTION: 0.20,
            ScoreMetric.HIERARCHY: 0.20
        }

    def _build_context_history(self, node_id: Optional[str]) -> List[Context]:
        if not node_id:
            return []
            
        contexts: List[Context] = []
        current_id = node_id
        depth = 0
        
        while current_id and depth < self.context_window:
            node = self.nodes[current_id]
            contexts.append(Context(
                prompt=node.prompt.content,
                thought=node.thought.content,
                depth=depth,
                node_id=node.id
            ))
            current_id = node.parent_id
            depth += 1
            
        return list(reversed(contexts))

    def _create_enhanced_prompt(self, prompt: str, context_history: List[Context]) -> str:
        if not context_history:
            return prompt
            
        context_text = "Previous context:\n"
        for ctx in context_history:
            context_text += f"\nDepth {ctx.depth}:\nQ: {ctx.prompt}\nA: {ctx.thought}\n"
            
        return f"{context_text}\nCurrent question: {prompt}\n\nProvide a thoughtful response that builds upon and maintains coherence with the previous context while addressing the current question."

    def _find_relations(self, node: Node):
        if self.debug:
            logger.info(f"Finding relations for node {node.id}")
            
        for other_node_id, other_node in self.nodes.items():
            if other_node_id != node.id:
                similarity = self._compute_similarity(node, other_node)
                if similarity > self.similarity_threshold:
                    if self.debug:
                        logger.debug(f"Found relation between {node.id} and {other_node_id} "
                                   f"with similarity {similarity}")
                    node.relations.append(other_node_id)
                    other_node.relations.append(node.id)

    def _compute_similarity(self, node1: Node, node2: Node) -> float:
        text1 = f"{node1.prompt.content} {node1.thought.content}"
        text2 = f"{node2.prompt.content} {node2.thought.content}"
        
        vectorizer = TfidfVectorizer(max_features=384)
        vectorizer.fit([text1, text2])
        emb1, emb2 = vectorizer.transform([text1, text2])
        
        similarity = float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
        
        if self.debug:
            logger.debug(f"Computed similarity: {similarity}")
        return similarity

    def _is_node_relevant(self, node: Node, prompt: str) -> bool:
        """
        Determines if a node is relevant to the current prompt using multiple criteria.

        Args:
            node (Node): The node to evaluate
            prompt (str): The current prompt text

        Returns:
            bool: True if the node is deemed relevant, False otherwise
        """
        # Create a temporary node for the prompt to enable comparison
        temp_node = Node(
            prompt=UserMessage(content=prompt),
            thought=AIMessage(content=""),
            context_history = []
        )

        # 1. Semantic Similarity Score (0-1)
        semantic_similarity = self._compute_similarity(node, temp_node)

        # 2. Key Concept Overlap Score (0-1)
        def extract_key_concepts(text: str) -> Set[str]:
            # Convert to lowercase and split into words
            words = text.lower().split()
            # Remove common stop words (expand this list as needed)
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'is', 'are'}
            # Keep only meaningful words that are at least 3 characters long
            return {word for word in words if word not in stop_words and len(word) >= 3}

        node_concepts = extract_key_concepts(f"{node.prompt.content} {node.thought.content}")
        prompt_concepts = extract_key_concepts(prompt)

        if not prompt_concepts:
            concept_overlap = 0.0
        else:
            concept_overlap = len(node_concepts.intersection(prompt_concepts)) / len(prompt_concepts)

        # 3. Context Continuity Score (0-1)
        context_score = 0.0
        if node.context_history:
            # Check if the prompt relates to the context history
            context_text = " ".join(
                ctx.prompt + " " + ctx.thought 
                for ctx in node.context_history
            )
            context_concepts = extract_key_concepts(context_text)
            if prompt_concepts:
                context_score = len(prompt_concepts.intersection(context_concepts)) / len(prompt_concepts)

        # 4. Depth Penalty (0.8-1.0)
        # Slightly decrease relevance for deeper nodes to prefer shallower, more direct connections
        depth = len(node.context_history) if node.context_history else 0
        depth_penalty = 1.0 - (depth * 0.05)  # 5% penalty per depth level, max 20% penalty
        depth_penalty = max(0.8, depth_penalty)  # Don't go below 0.8

        # 5. Recency Bonus (0-0.2)
        # Add a small bonus for more recent nodes
        recency_bonus = 0.0
        if hasattr(node, 'timestamp'):
            time_diff = time.time() - node.timestamp
            recency_bonus = max(0.0, 0.2 - (time_diff / (24 * 3600)))

        weights = {
            'semantic': 0.35,
            'concept': 0.25,
            'context': 0.20,
            'depth': 0.15,
            'recency': 0.05
        }

        final_score = (
            weights['semantic'] * semantic_similarity +
            weights['concept'] * concept_overlap +
            weights['context'] * context_score +
            weights['depth'] * depth_penalty +
            weights['recency'] * recency_bonus
        )

        if self.debug:
            logger.debug(f"""
            Node relevance scores for prompt '{prompt[:50]}...':
            - Semantic Similarity: {semantic_similarity:.3f}
            - Concept Overlap: {concept_overlap:.3f}
            - Context Continuity: {context_score:.3f}
            - Depth Penalty: {depth_penalty:.3f}
            - Recency Bonus: {recency_bonus:.3f}
            - Final Score: {final_score:.3f}
            - Threshold: {self.similarity_threshold}
            """)

        return final_score > self.similarity_threshold

    def expand(self, prompt: str, parent_id: Optional[str] = None, depth: int = 0) -> str:
        if self.debug:
            logger.info(f"Expanding prompt at depth {depth}")

        # Build context history
        context_history = self._build_context_history(parent_id)

        # Create enhanced prompt with context
        enhanced_prompt = self._create_enhanced_prompt(prompt, context_history)

        # Generate thought
        prompt_msg = AIMessage(content=prompt, model=self.llm.model_name, provider=self.llm.provider) if parent_id else UserMessage(content=prompt)

        template = self.template_manager.get_template("thought_generator")
        thought = self.llm.generate(template.format(context=enhanced_prompt))

        # Create and store node
        node = Node(
            prompt=prompt_msg,
            thought=thought,
            parent_id=parent_id,
            context_history=context_history,
        )

        if parent_id:
            self.nodes[parent_id].children.append(node.id)

        self.nodes[node.id] = node
        self._find_relations(node)

        # Check relevance of the newly created node
        if not self._is_node_relevant(node, prompt):
            if self.debug:
                logger.info(f"Deleting irrelevant node {node.id} related to prompt '{prompt}'")
            self._delete_node(node.id)
            return parent_id  # Return parent_id if the node is deleted

        # Generate follow-up questions if not at max depth
        if depth < self.max_iterations:
            template = self.template_manager.get_template("question_generator")
            questions = self.llm.generate(
                template.format(
                    context=enhanced_prompt,
                    response=thought.content,
                    num_questions=3
                )
            ).content.split("\n")

            for question in [q.strip() for q in questions if q.strip()]:
                _ = self.expand(question, node.id, depth + 1)

        return node.id

    def _delete_node(self, node_id: str) -> None:
        """Delete the node and clean up references."""
        if node_id in self.nodes:
            node = self.nodes[node_id]
            # Remove node from parent
            if node.parent_id and node.parent_id in self.nodes:
                self.nodes[node.parent_id].children.remove(node_id)
            # Remove node from children
            for child_id in node.children:
                if child_id in self.nodes:
                    self.nodes[child_id].parent_id = None  # Reset parent id of child nodes
            # Finally delete the node
            del self.nodes[node_id]
            if self.debug:
                logger.info(f"Node {node_id} wasn't relevent, deleted successfully.")

    def _compute_context_retention_score(self, path: List[str]) -> float:
        if len(path) < 2:
            return 1.0
            
        retention_scores = []
        for i in range(1, len(path)):
            current_node = self.nodes[path[i]]
            context_score = current_node._compute_context_retention_score()
            retention_scores.append(context_score)
            
        return np.mean(retention_scores)

    def _compute_hierarchy_score(self, path: List[str]) -> float:
        """
        Compute a score based on the strength of parent-child relationships in the path.
        Returns a value between 0 and 1, where 1 indicates strong hierarchical connections.
        """
        if len(path) < 2:
            return 1.0

        hierarchy_scores = []
        for i in range(len(path) - 1):
            current_node = self.nodes[path[i]]
            next_node = self.nodes[path[i + 1]]
            
            # Check if there's a direct parent-child relationship
            is_parent_child = (next_node.parent_id == current_node.id)
            
            if is_parent_child:
                # Calculate semantic similarity for parent-child relationship
                similarity = self._compute_similarity(current_node, next_node)
                # Weight parent-child relationships more heavily
                weighted_score = 0.7 + (0.3 * similarity)
            else:
                # For non-parent-child relationships, use a lower base score
                similarity = self._compute_similarity(current_node, next_node)
                weighted_score = 0.3 * similarity

            hierarchy_scores.append(weighted_score)
            
        return np.mean(hierarchy_scores)

    def _compute_relation_score(self, path: List[str]) -> float:
        """
        Compute a score based on lateral relationships between nodes in the path.
        """
        if len(path) < 2:
            return 1.0
            
        relation_scores = []
        for i in range(len(path)):
            current_node = self.nodes[path[i]]
            # Calculate how many nodes in the path are related to the current node
            related_nodes = set(current_node.relations).intersection(set(path))
            # Exclude parent-child relationships from lateral relations count
            if current_node.parent_id in related_nodes:
                related_nodes.remove(current_node.parent_id)
            for child_id in current_node.children:
                if child_id in related_nodes:
                    related_nodes.remove(child_id)
                    
            # Normalize the score based on potential relations
            potential_relations = len(path) - 1  # exclude self
            relation_score = len(related_nodes) / potential_relations if potential_relations > 0 else 0
            relation_scores.append(relation_score)
            
        return np.mean(relation_scores)

    def _compute_path_score(self, path: List[str]) -> PathScore:
        if self.debug:
            logger.info(f"Computing total path score for path of length {len(path)}")
            
        metrics = {
            ScoreMetric.DEPTH: np.mean([self.nodes[node_id].score for node_id in path]),
            ScoreMetric.RELATION: self._compute_relation_score(path),
            ScoreMetric.COHERENCE: self._compute_coherence_score(path),
            ScoreMetric.NOVELTY: self._compute_novelty_score(path),
            ScoreMetric.CONTEXT_RETENTION: self._compute_context_retention_score(path),
            ScoreMetric.HIERARCHY: self._compute_hierarchy_score(path)
        }
        
        total = sum(score * self.metric_weights[metric] for metric, score in metrics.items())
        
        if self.debug:
            logger.debug(f"""
            Path scoring breakdown:
            - Depth: {metrics[ScoreMetric.DEPTH]:.3f}
            - Relation: {metrics[ScoreMetric.RELATION]:.3f}
            - Coherence: {metrics[ScoreMetric.COHERENCE]:.3f}
            - Novelty: {metrics[ScoreMetric.NOVELTY]:.3f}
            - Context Retention: {metrics[ScoreMetric.CONTEXT_RETENTION]:.3f}
            - Hierarchy: {metrics[ScoreMetric.HIERARCHY]:.3f}
            - Total Score: {total:.3f}
            """)
            
        return PathScore(total=total, metrics=metrics)

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

    def _compute_novelty_score(self, path: List[str]) -> float:
        path_nodes = [self.nodes[node_id] for node_id in path]
        other_nodes = [node for node_id, node in self.nodes.items() if node_id not in path]
        
        if not other_nodes:
            return 0.5
            
        novelty_scores = []
        for path_node in path_nodes:
            similarities = [self._compute_similarity(path_node, other_node) 
                          for other_node in other_nodes]
            novelty_scores.append(1 - np.mean(similarities))
            
        return np.mean(novelty_scores)

    def pray(self, k: int = 3) -> Dict[str, List[Dict]]:
        if self.debug:
            logger.info(f"Starting pray operation with k={k}")
            
        root_nodes = [node_id for node_id, node in self.nodes.items() 
                     if node.parent_id is None]
        all_paths = []

        # Find all paths and compute scores
        for root_id in root_nodes:
            paths = []
            self._find_paths(root_id, set(), [], paths)

            for path in paths:
                path_score = self._compute_path_score(path)
                path_details = {
                    "path": path,
                    "score": path_score.total,
                    "metrics": {m.value: s for m, s in path_score.metrics.items()},
                    "trajectory": [
                        {
                            "node_id": node_id,
                            "prompt": self.nodes[node_id].prompt.content,
                            "thought": self.nodes[node_id].thought.content,
                            "context_retention": self.nodes[node_id]._compute_context_retention_score()
                        }
                        for node_id in path
                    ],
                }
                heapq.heappush(all_paths, (-path_score.total, path_details))

        # Get top k paths for each root
        top_k_paths = defaultdict(list)
        for _ in range(min(k, len(all_paths))):
            if all_paths:
                _, path_info = heapq.heappop(all_paths)
                root_id = path_info["path"][0]
                top_k_paths[root_id].append(path_info)

        return dict(top_k_paths)

    def _find_paths(self, start_id: str, visited: Set[str], path: List[str], 
                   paths: List[List[str]]):
        visited.add(start_id)
        path.append(start_id)

        node = self.nodes[start_id]
        if not node.children:
            paths.append(path.copy())
        else:
            for child_id in node.children:
                if child_id not in visited:
                    self._find_paths(child_id, visited, path, paths)

        visited.remove(start_id)
        path.pop()

    def miracle(self, k: int = 3) -> Dict[str, List[Dict]]:
        if self.debug:
            logger.info(f"Starting miracle operation with k={k}")
        prayer_results = self.pray(k)
        miracle_results = {}

        for root_id, paths in prayer_results.items():
            miracle_results[root_id] = []

            for path_info in paths:
                thoughts = [
                    f"Prompt: {node['prompt']}\nThought: {node['thought']}"
                    for node in path_info["trajectory"]
                ]

                template = self.template_manager.get_template("summary_generator")
                summary = self.llm.generate(template.format(thoughts="\n\n".join(thoughts)))

                result = {
                    "summary": summary.content,
                    "score": path_info["score"],
                    "metrics": path_info["metrics"],
                }
                miracle_results[root_id].append(result)

        return miracle_results
    
    def report(self) -> str:
        """
        Generate report based on the best trajectory that has the highest cumulative score.
        The report is generated by concatenating prompts and thoughts from each node 
        and passing them to the report generator.
        """
        if self.debug:
            logger.info(f"Generating report")
        
        prayer_results = self.pray(1)
        
        concatenated_thoughts = ""
        
        for path_info in prayer_results.values():
            for path in path_info:
                thoughts = [
                    f"Prompt: {node['prompt']}\nThought: {node['thought']}"
                    for node in path["trajectory"]
                ]
                
                concatenated_thoughts += "\n\n".join(thoughts)
        
        template = self.template_manager.get_template("report_generator")
        
        report = self.llm.generate(template.format(thoughts=concatenated_thoughts))
        
        return report.content

    def miracle_to_markdown(self, k: int = 3, output_dir: str = "./") -> None:
        if self.debug:
            logger.info(f"Starting miracle operation with k={k} and saving results as Markdown")
        prayer_results = self.pray(k)
        miracle_results = {}

        os.makedirs(output_dir, exist_ok=True)

        for root_id, paths in prayer_results.items():
            miracle_results[root_id] = []
            markdown_content = f"# Miracle Results for Root {root_id}\n\n"

            for i, path_info in enumerate(paths, start=1):
                thoughts = [
                    f"**Prompt:** {node['prompt']}\n\n**Thought:** {node['thought']}\n"
                    for node in path_info["trajectory"]
                ]

                template = self.template_manager.get_template("summary_generator")
                summary = self.llm.generate(template.format(thoughts="\n\n".join(thoughts)))

                result = {
                    "summary": summary.content,
                    "score": path_info["score"],
                    "metrics": path_info["metrics"],
                }
                miracle_results[root_id].append(result)

                markdown_content += f"## Path {i}\n\n"
                markdown_content += f"**Score:** {result['score']}\n\n"
                markdown_content += f"**Metrics:** {result['metrics']}\n\n"
                markdown_content += f"**Summary:**\n\n{result['summary']}\n\n"
                markdown_content += "---\n\n"

            output_file = os.path.join(output_dir, f"miracle_{root_id}.md")
            with open(output_file, "w") as f:
                f.write(markdown_content)

    def visualize(self) -> str:
        if self.debug:
            logger.info("Generating visualization")
        mermaid = ["graph TD"]
        for node_id, node in self.nodes.items():
            mermaid.append(f'{node_id}["{node.prompt.content[:20]}..."]')
            if node.parent_id:
                mermaid.append(f'{node.parent_id} --> {node_id}')

        return "\n".join(mermaid)