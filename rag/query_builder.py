from typing import Dict, List


class QueryBuilder:
    """Builds high-quality retrieval queries from statistical findings."""

    def build_query(self, finding: Dict[str, str]) -> str:
        parts = [
            finding.get("keyword", ""),
            finding.get("context", ""),
            "Potential employment discrimination",
            "Applicable federal and EEOC law",
            "Protected class analysis",
        ]

        if finding.get("suggested_focus"):
            parts.append(finding["suggested_focus"])

        return " . ".join([part for part in parts if part]).strip()
