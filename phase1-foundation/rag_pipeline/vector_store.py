"""
Vector storage module using Qdrant.
Handles vector database operations for storing and searching embeddings.
"""
from typing import List, Dict, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.models import Filter, FieldCondition, MatchValue
from shared.config.settings import settings
from shared.utils.logger import logger
import uuid

class VectorStore:
    """
    Manages vector storage operations using Qdrant.
    """
    
    def __init__(self, collection_name: str = None, use_memory: bool = True):
        """
        Initialize the vector store.
        
        Args:
            collection_name: Name of the collection in Qdrant
            use_memory: If True, use in-memory mode (for development)
        """
        self.collection_name = collection_name or settings.QDRANT_COLLECTION_NAME
        
        # Initialize Qdrant client
        if use_memory:
            # In-memory mode (no Docker needed for Day 1)
            self.client = QdrantClient(":memory:")
            logger.info("Qdrant client initialized in MEMORY mode")
        else:
            # Connect to Qdrant server
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            )
            logger.info(f"Qdrant client connected to {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
    
    def create_collection(self, vector_size: int = 1536):
        """
        Create a new collection in Qdrant.
        
        Args:
            vector_size: Dimension of the embedding vectors (1536 for OpenAI)
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            exists = any(col.name == self.collection_name for col in collections)
            
            if exists:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return
            
            # Create new collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE  # Cosine similarity for semantic search
                )
            )
            logger.info(f"Created collection '{self.collection_name}' with vector_size={vector_size}")
            
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise
    
    def add_documents(self, texts: List[str], embeddings: List[List[float]], 
                     metadata: List[Dict] = None):
        """
        Add documents with their embeddings to the vector store.
        
        Args:
            texts: List of text chunks
            embeddings: List of embedding vectors
            metadata: Optional list of metadata dictionaries
        """
        if len(texts) != len(embeddings):
            raise ValueError("Number of texts and embeddings must match")
        
        if metadata and len(metadata) != len(texts):
            raise ValueError("Number of metadata items must match number of texts")
        
        try:
            points = []
            for i, (text, embedding) in enumerate(zip(texts, embeddings)):
                point_id = str(uuid.uuid4())
                
                payload = {
                    'text': text,
                    'metadata': metadata[i] if metadata else {}
                }
                
                points.append(
                    PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=payload
                    )
                )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Added {len(points)} documents to collection '{self.collection_name}'")
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def search(self, query_embedding: List[float], top_k: int = None, 
               metadata_filter: Dict = None) -> List[Dict]:
        """
        Search for similar vectors in the store.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            metadata_filter: Optional metadata filter
            
        Returns:
            List of search results with text, score, and metadata
        """
        top_k = top_k or settings.TOP_K_RESULTS
        
        try:
            # Build filter if provided
            query_filter = None
            if metadata_filter:
                query_filter = Filter(
                    must=[
                        FieldCondition(
                            key=f"metadata.{key}",
                            match=MatchValue(value=value)
                        )
                        for key, value in metadata_filter.items()
                    ]
                )
            
            # Perform search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=query_filter
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'text': result.payload.get('text', ''),
                    'score': result.score,
                    'metadata': result.payload.get('metadata', {})
                })
            
            logger.info(f"Found {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching: {str(e)}")
            raise
    
    def get_collection_info(self) -> Dict:
        """
        Get information about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                'name': self.collection_name,
                'vectors_count': info.vectors_count,
                'points_count': info.points_count,
                'status': info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {}