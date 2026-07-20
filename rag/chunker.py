from typing import List

from .metadata import DocumentChunk, DocumentMetadata
from .utils import chunk_text_by_size


class Chunker:
    """Break legal text into focused chunks for embedding and retrieval."""

    def __init__(self, chunk_size: int = 300, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, document: DocumentChunk) -> List[DocumentChunk]:
        return self.chunk_text(document.text, document.metadata, document.metadata.document_id)

    def chunk_text(self, text: str, metadata: DocumentMetadata, document_id: str) -> List[DocumentChunk]:
        text_chunks = chunk_text_by_size(text, chunk_size=self.chunk_size, overlap=self.overlap)
        return [
            DocumentChunk(
                chunk_id=f"{document_id}_chunk_{index}",
                text=chunk_text,
                metadata=metadata,
            )
            for index, chunk_text in enumerate(text_chunks, start=1)
        ]
