from sqlalchemy import func
from sqlalchemy.orm import Session
from pgvector.sqlalchemy import Vector
from app.models.database_models import DocumentEmbedding, PathologyReport
from app.services.embedding_service import EmbeddingService
import numpy as np

class SearchService:
    """Service for semantic and keyword search"""
    
    @staticmethod
    def semantic_search(db: Session, query_text: str, top_k: int = 5) -> dict:
        """Search for documents semantically similar to query"""
        
        try:
            # Generate embedding for query
            embedding_service = EmbeddingService()
            result = embedding_service.generate_embedding(query_text)
            
            if result["status"] != "success":
                return {
                    "status": "error",
                    "message": "Failed to generate query embedding",
                    "results": []
                }
            
            query_embedding = result["embedding"]
            
            # PostgreSQL vector similarity search using L2 distance
            # Lower distance = more similar
            similar_docs = db.query(
                DocumentEmbedding,
                func.power(
                    func.sum(
                        func.power(
                            DocumentEmbedding.embedding - query_embedding,
                            2
                        )
                    ),
                    0.5
                ).label("distance")
            ).order_by("distance").limit(top_k).all()
            
            results = []
            for doc_emb, distance in similar_docs:
                # Convert distance to similarity score (0-1)
                # Using 1 / (1 + distance) formula
                similarity = 1 / (1 + float(distance))
                
                # Get pathology report data
                report = db.query(PathologyReport).filter(
                    PathologyReport.document_id == doc_emb.document_id
                ).first()
                
                results.append({
                    "document_id": doc_emb.document_id,
                    "similarity_score": round(similarity, 4),
                    "distance": round(float(distance), 4),
                    "text_preview": doc_emb.text_chunk[:200],
                    "test_type": report.test_type if report else "Unknown",
                    "diagnosis": report.diagnosis if report else "Unknown"
                })
            
            return {
                "status": "success",
                "query": query_text,
                "total_results": len(results),
                "results": results
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "results": []
            }
    
    @staticmethod
    def keyword_search(db: Session, keyword: str, top_k: int = 5) -> dict:
        """Simple keyword search"""
        
        try:
            # Search in pathology reports
            reports = db.query(PathologyReport).filter(
                (PathologyReport.diagnosis.ilike(f"%{keyword}%")) |
                (PathologyReport.summary.ilike(f"%{keyword}%")) |
                (PathologyReport.findings.ilike(f"%{keyword}%"))
            ).limit(top_k).all()
            
            results = []
            for report in reports:
                results.append({
                    "document_id": report.document_id,
                    "test_type": report.test_type,
                    "diagnosis": report.diagnosis,
                    "summary": report.summary[:200],
                    "patient_name": report.patient_name
                })
            
            return {
                "status": "success",
                "keyword": keyword,
                "total_results": len(results),
                "results": results
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "results": []
            }
