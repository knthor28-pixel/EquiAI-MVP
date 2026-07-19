from typing import Dict, List

from .chunker import Chunker
from .embedder import Embedder, DummyEmbedder
from .metadata import DocumentChunk, RetrievalResult
from .prompt_builder import PromptBuilder
from .query_builder import QueryBuilder
from .citation_formatter import CitationFormatter
from .vector_store import VectorStore
from .retriever import Retriever
from .reranker import Reranker
from .validator import Validator


class LegalRAGPipeline:
    """A concept pipeline for retrieval-augmented legal reasoning."""

    def __init__(
        self,
        embedder: Embedder = None,
        vector_store: VectorStore = None,
        chunker: Chunker = None,
        retriever: Retriever = None,
        reranker: Reranker = None,
        query_builder: QueryBuilder = None,
        prompt_builder: PromptBuilder = None,
        citation_formatter: CitationFormatter = None,
        validator: Validator = None,
    ):
        self.embedder = embedder or DummyEmbedder()
        self.vector_store = vector_store or VectorStore()
        self.chunker = chunker or Chunker()
        self.retriever = retriever or Retriever(self.embedder, self.vector_store)
        self.reranker = reranker or Reranker()
        self.query_builder = query_builder or QueryBuilder()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.citation_formatter = citation_formatter or CitationFormatter()
        self.validator = validator or Validator()

    def build_corpus(self, documents: List[Dict]) -> List[DocumentChunk]:
        from .loader import DocumentLoader

        loader = DocumentLoader()
        loaded = loader.load_documents(documents)
        chunks = []
        for document in loaded:
            chunks.extend(self.chunker.chunk_document(document))

        embeddings = self.embedder.embed_documents(chunks)
        self.vector_store.add_documents(chunks, embeddings)
        return chunks

    def build_query(self, finding: Dict[str, str]) -> str:
        return self.query_builder.build_query(finding)

    def retrieve(self, query: str, top_k: int = 20) -> List[RetrievalResult]:
        results = self.retriever.retrieve(query, top_k=top_k)
        return self.reranker.rank(query, results, top_k=5)

    def build_prompt(self, finding: Dict[str, str], retrieved: List[RetrievalResult]) -> str:
        return self.prompt_builder.build_prompt(finding, retrieved)

    def build_citations(self, retrieved: List[RetrievalResult]) -> List[str]:
        return self.citation_formatter.format_citations(retrieved)

    def validate(self, finding: Dict[str, str]) -> bool:
        return self.validator.validate_finding(finding)
