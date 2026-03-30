from openai import OpenAI
from app.config import settings
import numpy as np

class EmbeddingService:
    """Service for generating and managing embeddings"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"  # Cheaper model
        self.dimension = 1536
    
    def generate_embedding(self, text: str) -> dict:
        """Generate embedding for text"""
        try:
            if not settings.OPENAI_API_KEY:
                return {
                    "status": "error",
                    "message": "OpenAI API key not configured",
                    "embedding": None
                }
            
            # Remove extra whitespace
            text = text.strip()
            if len(text) == 0:
                return {
                    "status": "error",
                    "message": "Text cannot be empty",
                    "embedding": None
                }
            
            # Limit text to 8000 tokens (rough estimate: ~32000 characters)
            if len(text) > 32000:
                text = text[:32000]
            
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            
            embedding = response.data[0].embedding
            
            return {
                "status": "success",
                "embedding": embedding,
                "dimension": len(embedding),
                "cost_estimate": f"~${response.usage.prompt_tokens * 0.00002:.6f}"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "embedding": None
            }
    
    @staticmethod
    def cosine_similarity(vec1: list, vec2: list) -> float:
        """Calculate cosine similarity between two vectors"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    @staticmethod
    def normalize_vector(vec: list) -> list:
        """L2 normalize a vector"""
        vec = np.array(vec)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist()
