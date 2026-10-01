from fastapi import APIRouter
from .models import DocumentRequest
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()

generator = GeminiDocumentGenerator()


@router.post("/generate")
def generate_document(request: DocumentRequest):
    result = generator.generate_document(
        request.document_type,
        request.parties,
        request.terms,
        request.date
    )

    return {
        "document": result
    }