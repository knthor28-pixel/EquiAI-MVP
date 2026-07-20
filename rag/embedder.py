from abc import ABC, abstractmethod
from typing import List

from .metadata import DocumentChunk


class Embedder(ABC):
    """Abstract embedding interface for the RAG pipeline."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        raise NotImplementedError

    @abstractmethod
    def embed_documents(self, chunks: List[DocumentChunk]) -> List[List[float]]:
        raise NotImplementedError


class DummyEmbedder(Embedder):
    """Placeholder embedder for UI and initial development."""

    def embed_text(self, text: str) -> List[float]:
        return [float(len(text)) % 100] * 768

    def embed_documents(self, chunks: List[DocumentChunk]) -> List[List[float]]:
        return [self.embed_text(chunk.text) for chunk in chunks]
