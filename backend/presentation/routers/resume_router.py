"""Resume router — upload resume for AI analysis."""
from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile, status
from uuid import UUID

from application.dtos.dtos import ResumeUploadResponse
from presentation.dependencies.auth import get_current_user_id
from domain.entities.entities import User
from infrastructure.di.container import get_container

router = APIRouter(prefix="/resume", tags=["resume"])

ALLOWED = {"application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"}


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
):
    content = await file.read()
    mime = (file.content_type or "application/pdf").lower()
    if mime not in ALLOWED:
        from domain.exceptions import DomainException
        raise DomainException(f"Unsupported file type: {mime}", code="unsupported_file")
    return await get_container().upload_resume_use_case().execute(user_id, content, mime, file.filename)