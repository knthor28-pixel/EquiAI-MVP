import os
from typing import Dict, Iterable, List, Optional

from .metadata import DocumentChunk, DocumentMetadata
from .utils import normalize_text


class SourceLoader:
    """Recursively discovers and loads supported source documents (PDF, HTML, TXT).

    The loader derives simple metadata from the file path: the immediate subfolder
    under the source root is used as `jurisdiction` / `category` (e.g., federal, state).
    """

    SUPPORTED = (".pdf", ".txt", ".html", ".htm")

    def __init__(self, source_dir: str = "legal/source_documents"):
        self.source_dir = source_dir

    def _list_files(self) -> List[str]:
        matches: List[str] = []
        for root, _, files in os.walk(self.source_dir):
            for f in files:
                if f.lower().endswith(self.SUPPORTED):
                    matches.append(os.path.join(root, f))
        return matches

    def _derive_metadata(self, path: str) -> Dict[str, Optional[str]]:
        # jurisdiction/category heuristic: immediate subfolder under source_dir
        rel = os.path.relpath(path, self.source_dir)
        parts = rel.split(os.sep)
        category = parts[0] if len(parts) > 1 else "uncategorized"
        # map some common folder names
        jurisdiction = "United States"
        if category.lower() in ("state", "local"):
            jurisdiction = "State/Local"
        elif category.lower() in ("federal", "nist", "eeoc"):
            jurisdiction = "United States"
        return {"category": category, "jurisdiction": jurisdiction}

    def _load_pdf(self, path: str) -> str:
        # try PyMuPDF (fitz) first for higher quality extraction, fallback to PyPDF2
        text_parts: List[str] = []
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(path)
            for page in doc:
                try:
                    text_parts.append(page.get_text("text") or "")
                except Exception:
                    continue
            doc.close()
            return normalize_text("\n\n".join(text_parts))
        except Exception:
            try:
                from PyPDF2 import PdfReader

                reader = PdfReader(path)
                for page in reader.pages:
                    try:
                        text_parts.append(page.extract_text() or "")
                    except Exception:
                        continue
                return normalize_text("\n\n".join(text_parts))
            except Exception as exc:
                raise RuntimeError("No PDF extractor available (install PyMuPDF or PyPDF2)") from exc

    def _load_html(self, path: str) -> str:
        try:
            from bs4 import BeautifulSoup
        except Exception as exc:
            raise RuntimeError("BeautifulSoup4 is required to parse HTML. Install with 'pip install beautifulsoup4 lxml'") from exc

        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            soup = BeautifulSoup(fh, "lxml")

        # remove scripts/styles and typical boilerplate
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()

        texts = []
        for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            t = el.get_text(separator=" ", strip=True)
            if t:
                texts.append(t)
        return normalize_text("\n\n".join(texts))

    def _load_txt(self, path: str) -> str:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return normalize_text(fh.read())

    def load_file(self, path: str) -> Dict:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            text = self._load_pdf(path)
        elif ext in (".html", ".htm"):
            text = self._load_html(path)
        elif ext == ".txt":
            text = self._load_txt(path)
        else:
            return {}

        meta = self._derive_metadata(path)
        filename = os.path.splitext(os.path.basename(path))[0]
        return {
            "document_id": filename,
            "title": filename,
            "source": path,
            "jurisdiction": meta.get("jurisdiction"),
            "category": meta.get("category"),
            "text": text,
            "keywords": [],
            "protected_classes": [],
            "topics": [],
            "version": "imported",
        }

    def load_all(self) -> List[Dict]:
        files = self._list_files()
        docs: List[Dict] = []
        seen = set()
        for path in files:
            if path in seen:
                continue
            try:
                doc = self.load_file(path)
                if doc:
                    docs.append(doc)
            except Exception as exc:
                # keep going on errors; the pipeline will log details later
                continue
            seen.add(path)
        return docs
