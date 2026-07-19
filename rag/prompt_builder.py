from typing import List

from .metadata import RetrievalResult


class PromptBuilder:
    """Assembles the system prompt and user prompt for the reasoning model."""

    SYSTEM_TEMPLATE = """You are an employment-law compliance assistant.
Only use the retrieved legal materials.
Do not invent laws.
Do not give definitive legal advice.
Explain the statistical findings using the supplied legal references.
"""

    USER_TEMPLATE = """Finding
Keyword: {keyword}
Accepted: {accepted}
Rejected: {rejected}
Odds Ratio: {odds_ratio}

Retrieved Sources:
{sources}
"""

    def build_prompt(self, finding: dict, retrieved: List[RetrievalResult]) -> str:
        sources = "\n\n".join(
            f"[{index + 1}] {result.chunk.metadata.title} — {result.chunk.metadata.section or 'General'} ({result.chunk.metadata.jurisdiction})\n{result.chunk.text[:400]}..."
            for index, result in enumerate(retrieved)
        )
        return f"{self.SYSTEM_TEMPLATE}\n{self.USER_TEMPLATE.format(\
            keyword=finding.get('keyword', 'N/A'),\
            accepted=finding.get('accepted', 'N/A'),\
            rejected=finding.get('rejected', 'N/A'),\
            odds_ratio=finding.get('odds_ratio', 'N/A'),\
            sources=sources\
        )}"
