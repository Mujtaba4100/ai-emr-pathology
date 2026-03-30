from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.search_service import SearchService
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/search", tags=["search"])

class SemanticSearchRequest(BaseModel):
    query: str
    top_k: int = 5

class KeywordSearchRequest(BaseModel):
    keyword: str
    top_k: int = 5

@router.post("/semantic")
async def semantic_search(request: SemanticSearchRequest, db: Session = Depends(get_db)):
    """Semantic search endpoint"""
    
    # Validate inputs
    if not request.query or len(request.query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    if request.top_k < 1 or request.top_k > 50:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")
    
    try:
        result = SearchService.semantic_search(db, request.query, request.top_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/keyword")
async def keyword_search(request: KeywordSearchRequest, db: Session = Depends(get_db)):
    """Keyword search endpoint"""
    
    # Validate inputs
    if not request.keyword or len(request.keyword.strip()) == 0:
        raise HTTPException(status_code=400, detail="Keyword cannot be empty")
    
    if request.top_k < 1 or request.top_k > 50:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")
    
    try:
        result = SearchService.keyword_search(db, request.keyword, request.top_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/combined")
async def combined_search(request: SemanticSearchRequest, db: Session = Depends(get_db)):
    """Combined semantic and keyword search"""
    
    # Validate inputs
    if not request.query or len(request.query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    if request.top_k < 1 or request.top_k > 50:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")
    
    try:
        # Run both searches
        semantic_results = SearchService.semantic_search(db, request.query, request.top_k)
        keyword_results = SearchService.keyword_search(db, request.query, request.top_k)
        
        return {
            "status": "success",
            "query": request.query,
            "semantic_search": semantic_results,
            "keyword_search": keyword_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
