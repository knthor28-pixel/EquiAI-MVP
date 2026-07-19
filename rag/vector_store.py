from typing import Dict, List, Optional

from .metadata import DocumentChunk
from .utils import cosine_similarity


class VectorStore:
    """In-memory vector store for embedding search and retrieval."""

    def __init__(self):
        self.documents: Dict[str, DocumentChunk] = {}
        self.embeddings: Dict[str, List[float]] = {}

    def add_documents(self, chunks: List[DocumentChunk], embeddings: List[List[float]]) -> None:
        for chunk, embedding in zip(chunks, embeddings):
            self.documents[chunk.chunk_id] = chunk
            self.embeddings[chunk.chunk_id] = embedding

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[DocumentChunk]:
        scored = []
        for chunk_id, embedding in self.embeddings.items():
            score = cosine_similarity(query_embedding, embedding)
            scored.append((score, self.documents[chunk_id]))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:top_k]]

    def get(self, chunk_id: str) -> Optional[DocumentChunk]:
        return self.documents.get(chunk_id)
