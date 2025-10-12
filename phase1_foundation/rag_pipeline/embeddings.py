"""
Embedding generation module using OpenAI's embedding models.
Handles batch processing and caching for efficiency.
"""
from typing import List
from openai import OpenAI
from shared.config.settings import settings
from shared.utils.logger import logger

class EmbeddingGenerator:
    """
    Generates embeddings for text using OpenAI's embedding models.
    """
    
    def __init__(self, model: str = None):
        """
        Initialize the embedding generator.
        
        Args:
            model: OpenAI embedding model name
        """
        self.model = model or settings.EMBEDDING_MODEL
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        logger.info(f"EmbeddingGenerator initialized with model={self.model}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector (list of floats)
        """
        if not text or not text.strip():
            raise ValueError("Cannot generate embedding for empty text")
        
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text
            )
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding of dimension {len(embedding)}")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.
        More efficient than generating one at a time.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        # Remove empty texts
        texts = [t for t in texts if t and t.strip()]
        
        if not texts:
            raise ValueError("No valid texts provided for embedding generation")
        
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts")
            
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            
            embeddings = [item.embedding for item in response.data]
            logger.info(f"Successfully generated {len(embeddings)} embeddings")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            raise