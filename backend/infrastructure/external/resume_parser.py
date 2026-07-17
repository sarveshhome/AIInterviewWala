"""Resume parser — extracts raw text from PDF / DOCX."""
from __future__ import annotations

import io
import logging

from domain.exceptions import DomainException
from domain.interfaces.services import IResumeParser

logger = logging.getLogger(__name__)


class ResumeParser(IResumeParser):
    SUPPORTED = {
        "application/pdf": ".pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        "application/msword": ".doc",
        "text/plain": ".txt",
    }

    def parse(self, content: bytes, mime_type: str, file_name: str) -> str:
        mime_type = (mime_type or "").lower()
        try:
            if mime_type == "application/pdf" or file_name.lower().endswith(".pdf"):
                return self._parse_pdf(content)
            if "wordprocessingml" in mime_type or file_name.lower().endswith(".docx"):
                return self._parse_docx(content)
            if mime_type == "text/plain" or file_name.lower().endswith(".txt"):
                return content.decode("utf-8", errors="ignore")
        except Exception as exc:  # noqa: BLE001
            logger.exception("Resume parse failed for %s", file_name)
            raise DomainException(f"Failed to parse resume: {exc}", code="resume_parse_error") from exc
        raise DomainException(f"Unsupported resume type: {mime_type}", code="unsupported_resume")

    @staticmethod
    def _parse_pdf(content: bytes) -> str:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(content))
        return "\n".join((page.extract_text() or "") for page in reader.pages)

    @staticmethod
    def _parse_docx(content: bytes) -> str:
        from docx import Document
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())