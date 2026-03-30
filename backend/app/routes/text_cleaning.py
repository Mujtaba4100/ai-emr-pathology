from fastapi import APIRouter, HTTPException
from app.services.text_cleaner import TextCleaner
from app.schemas import TextCleanResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api/clean", tags=["text-cleaning"])

class CleanTextRequest(BaseModel):
    text: str

@router.post("/text", response_model=dict)
async def clean_text(request: CleanTextRequest):
    """Clean and normalize extracted text"""
    
    try:
        result = TextCleaner.clean_text(request.text)
        
        return {
            "status": result["status"],
            "original_preview": request.text[:200],
            "cleaned_preview": result["cleaned_text"][:200],
            "original_length": result["original_length"],
            "cleaned_length": result["cleaned_length"],
            "cleaned_text": result["cleaned_text"],
            "message": result["message"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
