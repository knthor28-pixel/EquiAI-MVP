from typing import Any, Dict


class Validator:
    """Validates the structure of the retrieval and prompt data."""

    def validate_finding(self, finding: Dict[str, Any]) -> bool:
        required_fields = ["keyword", "accepted", "rejected", "odds_ratio"]
        return all(field in finding and finding[field] is not None for field in required_fields)

    def validate_prompt(self, prompt: str) -> bool:
        return bool(prompt and len(prompt.strip()) > 0)
