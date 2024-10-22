from typing import List
import numpy as np
from collections import Counter
from math import log


class TfidfVectorizer:
    def __init__(self, max_features=384):
        self.max_features = max_features
        self.vocabulary_ = {}
        self.idf_ = {}
        self.fitted = False

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

    def transform(self, texts: List[str]) -> np.ndarray:
        if not self.fitted:
            self.fit(texts)

        result = np.zeros((len(texts), len(self.vocabulary_)))

        for i, text in enumerate(texts):
            words = Counter(text.lower().split())
            for word, count in words.items():
                if word in self.vocabulary_:
                    idx = self.vocabulary_[word]
                    tf = count / len(text.split())
                    result[i, idx] = tf * self.idf_.get(word, 0)

        return result
