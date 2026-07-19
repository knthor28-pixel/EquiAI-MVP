import os
from typing import Dict, Iterable, List

from .metadata import DocumentChunk, DocumentMetadata
from .utils import normalize_text


class PDFLoader:
    """Loads PDF source files into the RAG corpus."""

    def __init__(self, source_dir: str = "source"):
        self.source_dir = source_dir

    def _list_pdfs(self) -> List[str]:
        return [
            os.path.join(self.source_dir, filename)
            for filename in os.listdir(self.source_dir)
            if filename.lower().endswith(".pdf")
        ]

    def load_pdf(self, path: str) -> Dict:
        try:
            from PyPDF2 import PdfReader
        except ImportError as exc:
            raise RuntimeError(
                "PyPDF2 is required to read PDFs. Install it with 'pip install PyPDF2'."
            ) from exc

        reader = PdfReader(path)
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                continue

        text = normalize_text("\n\n".join(pages))
        return {
            "document_id": os.path.splitext(os.path.basename(path))[0],
            "title": os.path.splitext(os.path.basename(path))[0],
            "source": "PDF source",
            "jurisdiction": "United States",
            "category": "PDF Import",
            "text": text,
            "keywords": [],
            "protected_classes": [],
            "topics": [],
            "version": "imported",
        }

    def load_all(self) -> List[Dict]:
        pdfs = self._list_pdfs()
        return [self.load_pdf(path) for path in pdfs]
