"""
PDF processing implementation using pdfplumber and PyPDF2.
This service extracts text content from uploaded PDF files.
"""

import io
import logging
from typing import Optional

import pdfplumber
import PyPDF2

from ...domain.services import PDFProcessingService

logger = logging.getLogger(__name__)


class PDFProcessor(PDFProcessingService):
    """Concrete implementation of PDF processing service."""

    async def extract_text_from_pdf(self, file_content: bytes) -> str:
        """
        Extract text content from PDF file using multiple strategies.
        First tries pdfplumber, falls back to PyPDF2 if needed.
        """
        try:
            # Strategy 1: Try pdfplumber (better for complex layouts)
            text = await self._extract_with_pdfplumber(file_content)
            if text and text.strip():
                logger.info("Successfully extracted text using pdfplumber")
                return text

            # Strategy 2: Fallback to PyPDF2
            text = await self._extract_with_pypdf2(file_content)
            if text and text.strip():
                logger.info("Successfully extracted text using PyPDF2")
                return text

            # If both methods fail
            logger.warning("Could not extract meaningful text from PDF")
            return ""

        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise PDFProcessingError(f"Failed to extract text: {str(e)}")

    async def validate_pdf_file(self, file_content: bytes) -> bool:
        """Validate if the file is a proper PDF."""
        try:
            # Check PDF header
            if not file_content.startswith(b"%PDF-"):
                return False

            # Try to open with PyPDF2 for basic validation
            pdf_stream = io.BytesIO(file_content)
            reader = PyPDF2.PdfReader(pdf_stream)

            # Check if we can access basic properties
            num_pages = len(reader.pages)

            return num_pages > 0

        except Exception as e:
            logger.warning(f"PDF validation failed: {str(e)}")
            return False

    async def _extract_with_pdfplumber(self, file_content: bytes) -> str:
        """Extract text using pdfplumber (better for tables and layouts)."""
        try:
            pdf_stream = io.BytesIO(file_content)
            text_parts = []

            with pdfplumber.open(pdf_stream) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)

            return "\n".join(text_parts)

        except Exception as e:
            logger.debug(f"pdfplumber extraction failed: {str(e)}")
            return ""

    async def _extract_with_pypdf2(self, file_content: bytes) -> str:
        """Extract text using PyPDF2 (fallback method)."""
        try:
            pdf_stream = io.BytesIO(file_content)
            reader = PyPDF2.PdfReader(pdf_stream)
            text_parts = []

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

            return "\n".join(text_parts)

        except Exception as e:
            logger.debug(f"PyPDF2 extraction failed: {str(e)}")
            return ""

    def get_pdf_metadata(self, file_content: bytes) -> Optional[dict]:
        """Extract metadata from PDF file."""
        try:
            pdf_stream = io.BytesIO(file_content)
            reader = PyPDF2.PdfReader(pdf_stream)

            metadata = {
                "pages": len(reader.pages),
                "title": (
                    getattr(reader.metadata, "title", None)
                    if reader.metadata
                    else None
                ),
                "author": (
                    getattr(reader.metadata, "author", None)
                    if reader.metadata
                    else None
                ),
                "creator": (
                    getattr(reader.metadata, "creator", None)
                    if reader.metadata
                    else None
                ),
                "producer": (
                    getattr(reader.metadata, "producer", None)
                    if reader.metadata
                    else None
                ),
            }

            return metadata

        except Exception as e:
            logger.warning(f"Could not extract PDF metadata: {str(e)}")
            return None


class PDFProcessingError(Exception):
    """Custom exception for PDF processing errors."""

    pass
