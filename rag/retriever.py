from typing import List

from .embedder import Embedder
from .metadata import DocumentChunk, RetrievalResult
from .vector_store import VectorStore


class Retriever:
    """Two-stage retrieval pipeline for legal reasoning evidence."""

    def __init__(self, embedder: Embedder, vector_store: VectorStore):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 20) -> List[RetrievalResult]:
        query_embedding = self.embedder.embed_text(query)
        chunks = self.vector_store.search(query_embedding, top_k=top_k)
        return [RetrievalResult(chunk=chunk, score=1.0) for chunk in chunks]
