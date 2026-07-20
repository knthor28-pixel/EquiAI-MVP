from typing import List

from .metadata import RetrievalResult


class CitationFormatter:
    """Formats citations for the final reasoning output."""

    def format_citations(self, results: List[RetrievalResult]) -> List[str]:
        return [
            f"{index + 1}. {result.chunk.metadata.title} — {result.chunk.metadata.section or 'General'} ({result.chunk.metadata.jurisdiction})"
            for index, result in enumerate(results)
        ]
