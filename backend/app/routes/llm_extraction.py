from fastapi import APIRouter, HTTPException
from app.services.llm_extractor import LLMExtractor
from pydantic import BaseModel

router = APIRouter(prefix="/api/extract", tags=["llm-extraction"])

class ExtractRequest(BaseModel):
    cleaned_text: str

@router.post("/medical-data")
async def extract_medical_data(request: ExtractRequest):
    """Extract structured medical data from cleaned text using LLM"""
    
    try:
        extractor = LLMExtractor()
        result = extractor.extract_from_text(request.cleaned_text)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test")
async def test_extraction():
    """Test LLM extraction with sample data"""
    
    sample_text = """
    Patient: John Doe
    Test Date: 2026-03-28
    Test Type: Complete Blood Count (CBC)
    
    Findings:
    - Hemoglobin: 14.5 g/dL (Normal: 13.5-17.5)
    - White Blood Cells: 7.2 x10^3/µL (Normal: 4.5-11.0)
    - Platelets: 250 x10^3/µL (Normal: 150-400)
    
    Diagnosis: No abnormalities detected
    """
    
    try:
        extractor = LLMExtractor()
        result = extractor.extract_from_text(sample_text)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
