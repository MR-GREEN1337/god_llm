from typing import Dict, Tuple
from god_llm.plugins.base import BaseLLM
from loguru import logger


class QuestionEvaluator:
    def __init__(self, llm: BaseLLM, debug: bool = False):
        """
        Initialize the QuestionEvaluator with logging capabilities.
        
        Args:
            llm (BaseLLM): The language model instance to use for evaluation
            debug (bool): Flag to enable or disable debug logging
        """
        self.llm = llm
        self.debug = debug
        
        # Initialize logging if debug mode is enabled
        if self.debug:
            # Remove any existing handlers to avoid duplicates
            logger.remove()
            
            # Add a file handler for detailed logging
            logger.add(
                "question_evaluator.log",
                rotation="10 MB",
                level="DEBUG",
                format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
                backtrace=True,
                diagnose=True
            )
            
            # Add a console handler for immediate feedback
            logger.add(
                lambda msg: print(msg),
                level="INFO",
                format="{time:HH:mm:ss} | {level} | {message}"
            )
            
            logger.info("QuestionEvaluator initialized in debug mode")
        
    def evaluate_question(self, question: str, context: str, previous_thought: str) -> Tuple[float, Dict[str, float]]:
        """
        Evaluate a generated question based on multiple criteria.
        Returns a total score and individual metric scores.
        """
        if self.debug:
            logger.debug(f"\nEvaluating question: {question}\nContext length: {len(context)}\nPrevious thought length: {len(previous_thought)}")
        
        scores = {}
        for metric in ['relevance', 'depth', 'novelty', 'clarity', 'actionability']:
            if self.debug:
                logger.debug(f"Calculating {metric} score...")
                
            try:
                score_method = getattr(self, f"_score_{metric}")
                scores[metric] = score_method(question, context, previous_thought)
                
                if self.debug:
                    logger.debug(f"{metric.capitalize()} score: {scores[metric]:.3f}")
                    
            except Exception as e:
                logger.error(f"Error calculating {metric} score: {str(e)}")
                scores[metric] = 0.0
        
        # Weights for different aspects
        weights = {
            'relevance': 0.3,
            'depth': 0.25,
            'novelty': 0.2,
            'clarity': 0.15,
            'actionability': 0.1
        }
        
        total_score = sum(score * weights[metric] for metric, score in scores.items())
        
        if self.debug:
            logger.info(f"""
            Question Evaluation Summary:
            Question: {question}
            Scores:
                - Relevance: {scores['relevance']:.3f} (weight: {weights['relevance']})
                - Depth: {scores['depth']:.3f} (weight: {weights['depth']})
                - Novelty: {scores['novelty']:.3f} (weight: {weights['novelty']})
                - Clarity: {scores['clarity']:.3f} (weight: {weights['clarity']})
                - Actionability: {scores['actionability']:.3f} (weight: {weights['actionability']})
            Total Score: {total_score:.3f}
            """)
        
        return total_score, scores
        
    def _score_relevance(self, question: str, context: str, previous_thought: str) -> float:
        """Score how well the question relates to the context and previous thought."""
        if self.debug:
            logger.debug("Scoring relevance...")
            
        template = """
            Rate how relevant this follow-up question is to the given context and previous response.
            Consider:
            1. Does it build upon key concepts from the context?
            2. Does it explore important implications from the previous response?
            3. Is it meaningfully connected to the main topic?

            Context: {context}
            Previous Response: {previous_thought}
            Question: {question}

            Please return **only** a numerical score between 0 and 1. Do not include any additional text or explanation. Only the score should be returned as a number.
            """

        
        try:
            score = float(self.llm.generate(
                template.format(
                    context=context,
                    previous_thought=previous_thought,
                    question=question
                )
            ).content.strip())
            
            if self.debug:
                logger.debug(f"Relevance score calculated: {score:.3f}")
            
            return score
            
        except Exception as e:
            logger.error(f"Error in relevance scoring: {str(e)}")
            return 0.0
        
    def _score_depth(self, question: str, context: str, previous_thought: str) -> float:
        """Score the intellectual depth and complexity of the question."""
        if self.debug:
            logger.debug("Scoring depth...")
            
        template = """
            Rate the intellectual depth of this question.
            Consider:
            1. Does it require critical thinking?
            2. Does it explore underlying principles or mechanisms?
            3. Does it connect multiple concepts?
            4. Does it encourage analysis rather than simple recall?

            Question: {question}

            Please return **only** a numerical score between 0 and 1. Do not include any additional text or explanation. Only the score should be returned as a number.
            """

        
        try:
            score = float(self.llm.generate(
                template.format(question=question)
            ).content.strip())
            
            if self.debug:
                logger.debug(f"Depth score calculated: {score:.3f}")
            
            return score
            
        except Exception as e:
            logger.error(f"Error in depth scoring: {str(e)}")
            return 0.0
        
    def _score_novelty(self, question: str, context: str, previous_thought: str) -> float:
        """Score how much the question brings new perspectives or angles."""
        if self.debug:
            logger.debug("Scoring novelty...")
            
        template = """
            Rate how much this question brings new perspectives while remaining relevant.
            Consider:
            1. Does it explore uncovered aspects of the topic?
            2. Does it approach the subject from a fresh angle?
            3. Does it avoid redundancy with the context and previous response?

            Context: {context}
            Previous Response: {previous_thought}
            Question: {question}

            Please return **only** a numerical score between 0 and 1. Do not include any additional text or explanation. Only the score should be returned as a number.
            """

        
        try:
            score = float(self.llm.generate(
                template.format(
                    context=context,
                    previous_thought=previous_thought,
                    question=question
                )
            ).content.strip())
            
            if self.debug:
                logger.debug(f"Novelty score calculated: {score:.3f}")
            
            return score
            
        except Exception as e:
            logger.error(f"Error in novelty scoring: {str(e)}")
            return 0.0
        
    def _score_clarity(self, question: str, context: str, previous_thought: str) -> float:
        """Score how clear and well-formulated the question is."""
        if self.debug:
            logger.debug("Scoring clarity...")
            
        template = """
            Rate the clarity of this question.
            Consider:
            1. Is it clearly articulated?
            2. Is it specific enough to be answerable?
            3. Does it avoid ambiguity?
            4. Is it properly structured?

            Question: {question}

            Please return **only** a numerical score between 0 and 1. Do not include any additional text or explanation. Only the score should be returned as a number.
            """

        
        try:
            score = float(self.llm.generate(
                template.format(question=question)
            ).content.strip())
            
            if self.debug:
                logger.debug(f"Clarity score calculated: {score:.3f}")
            
            return score
            
        except Exception as e:
            logger.error(f"Error in clarity scoring: {str(e)}")
            return 0.0
        
    def _score_actionability(self, question: str, context: str, previous_thought: str) -> float:
        """Score how actionable and answerable the question is."""
        if self.debug:
            logger.debug("Scoring actionability...")
            
        template = """
            Rate how actionable this question is.
            Consider:
            1. Can it be meaningfully answered?
            2. Does it have a clear scope?
            3. Would the answer provide valuable insights?
            4. Is it neither too broad nor too narrow?

            Question: {question}

            Please return **only** a numerical score between 0 and 1. Do not include any additional text or explanation. Only the score should be returned as a number.
            """

        
        try:
            score = float(self.llm.generate(
                template.format(question=question)
            ).content.strip())
            
            if self.debug:
                logger.debug(f"Actionability score calculated: {score:.3f}")
            
            return score
            
        except Exception as e:
            logger.error(f"Error in actionability scoring: {str(e)}")
            return 0.0