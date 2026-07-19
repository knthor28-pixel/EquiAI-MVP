from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class DocumentMetadata:
    document_id: str
    title: str
    source: str
    jurisdiction: str
    category: str
    publication_date: Optional[str] = None
    effective_date: Optional[str] = None
    section: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    protected_classes: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    version: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DocumentChunk:
    chunk_id: str
    text: str
    metadata: DocumentMetadata
    embedding: Optional[List[float]] = None

@dataclass
class RetrievalResult:
    chunk: DocumentChunk
    score: float
