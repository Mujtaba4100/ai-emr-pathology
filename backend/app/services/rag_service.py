from openai import OpenAI
from app.config import settings
from sqlalchemy.orm import Session
from app.services.search_service import SearchService
import json

class RAGService:
    """RAG (Retrieval Augmented Generation) service for chatbot"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"
    
    @staticmethod
    def format_search_results(search_results: list) -> str:
        """Format search results as context"""
        context = "RELEVANT DOCUMENTS:\n\n"
        for i, result in enumerate(search_results, 1):
            context += f"{i}. Test Type: {result.get('test_type', 'Unknown')}\n"
            context += f"   Similarity: {result.get('similarity_score', 0):.2%}\n"
            context += f"   Preview: {result.get('text_preview', '')}\n"
            context += f"   Diagnosis: {result.get('diagnosis', 'Unknown')}\n\n"
        return context
    
    def answer_question(self, db: Session, question: str, conversation_history: list = None) -> dict:
        """Answer user question using RAG"""
        
        try:
            if not settings.OPENAI_API_KEY:
                return {
                    "status": "error",
                    "message": "OpenAI API key not configured",
                    "answer": None
                }
            
            # Search for relevant documents
            search_result = SearchService.semantic_search(db, question, top_k=3)
            
            if search_result["status"] != "success" or len(search_result["results"]) == 0:
                return {
                    "status": "no_results",
                    "message": "No relevant documents found",
                    "answer": "I could not find relevant documents to answer your question.",
                    "source_documents": []
                }
            
            # Format context from search results
            context = self.format_search_results(search_result["results"])
            
            # Build conversation
            if conversation_history is None:
                conversation_history = []
            
            # Add context and new question
            system_message = """You are a medical AI assistant that answers questions about pathology reports based on retrieved documents.
            
Rules:
1. ONLY answer based on the provided documents
2. If the answer is not in the documents, say "I don't have this information in the available documents"
3. Be concise and medically accurate
4. Always cite which document the answer comes from
5. Do not make up or hallucinate information"""
            
            user_message = f"{context}\n\nQuestion: {question}\n\nBased on the documents above, please answer this question."
            
            messages = [
                {"role": "system", "content": system_message}
            ]
            
            # Add conversation history
            for msg in conversation_history:
                messages.append(msg)
            
            # Add current question
            messages.append({"role": "user", "content": user_message})
            
            # Get response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,  # Lower temp for consistency
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            return {
                "status": "success",
                "answer": answer,
                "source_documents": search_result["results"],
                "total_sources": len(search_result["results"]),
                "cost_estimate": f"~${response.usage.prompt_tokens * 0.0005 / 1000:.4f}"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "answer": None
            }
