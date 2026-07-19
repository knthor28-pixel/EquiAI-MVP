from typing import List

from .metadata import RetrievalResult


class Reranker:
    """Simple re-ranker for retrieved legal chunks."""

    def rank(self, query: str, results: List[RetrievalResult], top_k: int = 5) -> List[RetrievalResult]:
        ranked = sorted(results, key=lambda result: result.score, reverse=True)
        return ranked[:top_k]
