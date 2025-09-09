"""
API routes for CV management.
"""

import logging
import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from ....config import settings
from ....infrastructure.ai import AIServiceError, create_ai_service
from ....infrastructure.pdf import PDFProcessingError, PDFProcessor
from ...schemas import CVUploadResponse

logger = logging.getLogger(__name__)

cv_router = APIRouter()


def get_pdf_processor():
    """Dependency to get PDF processor."""
    return PDFProcessor()


def get_ai_service():
    """Dependency to get AI service."""
    try:
        return create_ai_service()
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))


@cv_router.post("/upload", response_model=CVUploadResponse)
async def upload_cv(
    file: UploadFile = File(...),
    pdf_processor: PDFProcessor = Depends(get_pdf_processor),
    ai_service=Depends(get_ai_service),
):
    """
    Upload and analyze a CV file.
    Accepts PDF files and extracts structured data using AI.
    """
    try:
        # Validate file type
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400, detail="Only PDF files are supported"
            )

        # Read file content
        file_content = await file.read()

        # Validate file size
        if len(file_content) > settings.max_file_size_bytes:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"File too large. Maximum size: "
                    f"{settings.max_file_size_mb}MB"
                ),
            )

        # Validate PDF
        if not await pdf_processor.validate_pdf_file(file_content):
            raise HTTPException(status_code=400, detail="Invalid PDF file")

        # Extract text from PDF
        raw_text = await pdf_processor.extract_text_from_pdf(file_content)

        if not raw_text.strip():
            raise HTTPException(
                status_code=400, detail="Could not extract text from PDF"
            )

        # Extract structured data using AI
        cv = await ai_service.extract_cv_data(raw_text)
        cv.id = str(uuid.uuid4())
        cv.filename = file.filename

        # Save file to uploads directory
        if not os.path.exists(settings.upload_dir):
            os.makedirs(settings.upload_dir)

        file_path = os.path.join(
            settings.upload_dir, f"{cv.id}_{file.filename}"
        )
        with open(file_path, "wb") as f:
            f.write(file_content)

        logger.info(f"Successfully processed CV: {cv.id}")

        return CVUploadResponse(
            id=cv.id,
            filename=cv.filename,
            message="CV uploaded and analyzed successfully",
            extracted_data={
                "name": cv.name,
                "email": cv.email,
                "skills": [
                    {"name": s.name, "level": s.level.value} for s in cv.skills
                ],
                "experience_years": cv.total_experience_years,
                "education": [
                    {"degree": e.degree, "institution": e.institution}
                    for e in cv.education
                ],
                "certifications": cv.certifications,
            },
        )

    except PDFProcessingError as e:
        logger.error(f"PDF processing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except AIServiceError as e:
        logger.error(f"AI service error: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error processing CV: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@cv_router.get("/")
async def list_cvs():
    """List all uploaded CVs (placeholder for future database integration)."""
    return {"message": "CV listing not yet implemented"}
