from typing import Dict, Iterable, List

from .metadata import DocumentChunk, DocumentMetadata


class DocumentLoader:
    """Load structured legal documents into the RAG corpus."""

    def load_documents(self, documents: Iterable[Dict]) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []
        for raw in documents:
            metadata = DocumentMetadata(
                document_id=raw.get("document_id", raw.get("title", "unknown")),
                title=raw.get("title", "Untitled Document"),
                source=raw.get("source", "unknown"),
                jurisdiction=raw.get("jurisdiction", "global"),
                category=raw.get("category", "uncategorized"),
                publication_date=raw.get("publication_date"),
                effective_date=raw.get("effective_date"),
                section=raw.get("section"),
                keywords=raw.get("keywords", []),
                protected_classes=raw.get("protected_classes", []),
                topics=raw.get("topics", []),
                version=raw.get("version"),
                extra=raw.get("extra", {}),
            )
            text = raw.get("text", "")
            chunk = DocumentChunk(
                chunk_id=f"{metadata.document_id}_base",
                text=text,
                metadata=metadata,
            )
            chunks.append(chunk)
        return chunks
