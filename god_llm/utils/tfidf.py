from typing import List, Tuple
import numpy as np
from collections import Counter
from math import log
from functools import lru_cache

class TfidfVectorizer:
    def __init__(self, max_features=384, cache_size=128):
        self.max_features = max_features
        self.vocabulary_ = {}
        self.idf_ = {}
        self.fitted = False
        self.cache_size = cache_size
        # Initialize the cached transform method
        self._cached_transform = lru_cache(maxsize=cache_size)(self._transform_single)
        
    def fit(self, texts: List[str]):
        word_doc_count = Counter()
        all_words = Counter()

        for text in texts:
            words = Counter(text.lower().split())
            for word in words:
                word_doc_count[word] += 1
            all_words.update(words)

        self.vocabulary_ = {
            word: idx
            for idx, (word, _) in enumerate(all_words.most_common(self.max_features))
        }

        num_docs = len(texts)
        self.idf_ = {
            word: log(num_docs / (count + 1)) + 1
            for word, count in word_doc_count.items()
            if word in self.vocabulary_
        }
        self.fitted = True
        
        # Clear the cache when fitting new data
        self._cached_transform.cache_clear()
        
    def _transform_single(self, text: str) -> Tuple[float, ...]:
        """Transform a single text into a TF-IDF vector.
        Returns a tuple for hashability (required for lru_cache)."""
        if not self.fitted:
            raise ValueError("Vectorizer must be fitted before transform")
            
        vector = np.zeros(len(self.vocabulary_))
        words = Counter(text.lower().split())
        
        for word, count in words.items():
            if word in self.vocabulary_:
                idx = self.vocabulary_[word]
                tf = count / len(text.split())
                vector[idx] = tf * self.idf_.get(word, 0)
                
        return tuple(vector)

    def transform(self, texts: List[str]) -> np.ndarray:
        """Transform a list of texts into TF-IDF vectors."""
        if not self.fitted:
            self.fit(texts)
            
        # Transform texts using the cached method
        result = np.array([self._cached_transform(text) for text in texts])
        return result
    
    def clear_cache(self):
        """Manually clear the transform cache"""
        self._cached_transform.cache_clear()
    
    def get_cache_info(self):
        """Get information about the cache performance"""
        return self._cached_transform.cache_info()
    
    def __getstate__(self):
        """Custom serialization method to handle cache serialization"""
        state = self.__dict__.copy()
        # Remove the cached transform function before serialization
        state.pop('_cached_transform', None)
        return state
    
    def __setstate__(self, state):
        """Custom deserialization method to restore cache functionality"""
        self.__dict__.update(state)
        # Restore the cached transform function
        self._cached_transform = lru_cache(maxsize=self.cache_size)(self._transform_single)