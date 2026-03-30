from fastapi import APIRouter, HTTPException, Depends
from app.services.embedding_service import EmbeddingService
from app.database import get_db
from app.services.database_service import DatabaseService
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter(prefix="/api/embeddings", tags=["embeddings"])

class EmbeddingRequest(BaseModel):
    text: str
    file_id: str = None

class SimilarityRequest(BaseModel):
    text1: str
    text2: str

@router.post("/generate")
async def generate_embedding(request: EmbeddingRequest, db: Session = Depends(get_db)):
    """Generate embedding for text"""
    
    try:
        service = EmbeddingService()
        result = service.generate_embedding(request.text)
        
        # Save to database if file_id provided
        if request.file_id and result["status"] == "success":
            try:
                DatabaseService.save_embedding(
                    db,
                    file_id=request.file_id,
                    embedding=result["embedding"],
                    text_chunk=request.text[:500]  # Save preview
                )
            except Exception as db_error:
                # Embedding generated but database save failed
                pass
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/similarity")
async def calculate_similarity(request: SimilarityRequest):
    """Calculate similarity between two texts"""
    
    try:
        service = EmbeddingService()
        
        emb1 = service.generate_embedding(request.text1)
        emb2 = service.generate_embedding(request.text2)
        
        if emb1["status"] != "success" or emb2["status"] != "success":
            return {"status": "error", "message": "Failed to generate embeddings"}
        
        similarity = EmbeddingService.cosine_similarity(
            emb1["embedding"],
            emb2["embedding"]
        )
        
        return {
            "status": "success",
            "similarity_score": float(similarity),
            "similarity_percentage": f"{similarity * 100:.2f}%",
            "message": f"Similarity: {similarity * 100:.2f}%"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test")
async def test_embedding():
    """Test embedding generation with sample medical text"""
    
    sample_text = """
    PATHOLOGY REPORT
    Test: Complete Blood Count (CBC)
    Hemoglobin: 14.5 g/dL (Normal: 13.5-17.5)
    White Blood Cells: 7.2 x10^3/µL (Normal: 4.5-11.0)
    Platelets: 250 x10^3/µL (Normal: 150-400)
    """
    
    try:
        service = EmbeddingService()
        result = service.generate_embedding(sample_text)
        
        if result["status"] == "success":
            return {
                "status": "success",
                "message": "Test embedding generated successfully",
                "dimension": result["dimension"],
                "embedding_sample": result["embedding"][:5],  # First 5 dimensions
                "cost_estimate": result["cost_estimate"]
            }
        else:
            return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
