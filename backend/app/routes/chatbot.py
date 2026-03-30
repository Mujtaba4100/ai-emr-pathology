from fastapi import APIRouter, HTTPException, Depends
from app.services.rag_service import RAGService
from app.database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/chat", tags=["chatbot"])

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    question: str
    conversation_history: List[ChatMessage] = []

@router.post("/ask")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Ask question to medical chatbot"""
    
    try:
        rag_service = RAGService()
        
        # Convert to openai format
        history = [{"role": msg.role, "content": msg.content} for msg in request.conversation_history]
        
        result = rag_service.answer_question(db, request.question, history)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test")
async def test_chat(db: Session = Depends(get_db)):
    """Test chatbot with sample question"""
    
    try:
        rag_service = RAGService()
        result = rag_service.answer_question(db, "What is the most common finding in the reports?")
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
