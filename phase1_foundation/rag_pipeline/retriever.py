"""
Retrieval module that orchestrates the complete RAG pipeline.
Combines document processing, embedding, storage, and LLM generation.
"""
from typing import List, Dict, Optional
from openai import OpenAI
from .document_processor import DocumentProcessor
from .embeddings import EmbeddingGenerator
from .vector_store import VectorStore
from shared.config.settings import settings
from shared.utils.logger import logger

class RAGRetriever:
    """
    Complete RAG pipeline that retrieves relevant context and generates responses.
    """
    
    def __init__(self):
        """Initialize all components of the RAG pipeline"""
        self.doc_processor = DocumentProcessor()
        self.embedding_gen = EmbeddingGenerator()
        self.vector_store = VectorStore(use_memory=True)
        self.llm_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Create collection
        self.vector_store.create_collection()
        
        logger.info("RAGRetriever initialized successfully")
    
    def ingest_documents(self, file_paths: List[str] = None, texts: List[str] = None,
                        metadata: List[Dict] = None):
        """
        Ingest documents into the RAG system.
        
        Args:
            file_paths: List of file paths to ingest
            texts: List of raw texts to ingest (alternative to file_paths)
            metadata: Optional metadata for each document
        """
        all_chunks = []
        
        # Process files
        if file_paths:
            for file_path in file_paths:
                try:
                    chunks = self.doc_processor.process_file(file_path)
                    all_chunks.extend(chunks)
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")
                    continue
        
        # Process raw texts
        if texts:
            for i, text in enumerate(texts):
                meta = metadata[i] if metadata and i < len(metadata) else {}
                chunks = self.doc_processor.chunk_text(text, meta)
                all_chunks.extend(chunks)
        
        if not all_chunks:
            logger.warning("No chunks to ingest")
            return
        
        # Extract texts and metadata
        chunk_texts = [chunk['text'] for chunk in all_chunks]
        chunk_metadata = [chunk['metadata'] for chunk in all_chunks]
        
        # Generate embeddings in batch
        logger.info(f"Generating embeddings for {len(chunk_texts)} chunks...")
        embeddings = self.embedding_gen.generate_embeddings_batch(chunk_texts)
        
        # Store in vector database
        logger.info("Storing in vector database...")
        self.vector_store.add_documents(chunk_texts, embeddings, chunk_metadata)
        
        logger.info(f"Successfully ingested {len(all_chunks)} chunks")
    
    def retrieve(self, query: str, top_k: int = None, 
                metadata_filter: Dict = None) -> List[Dict]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Search query
            top_k: Number of results to return
            metadata_filter: Optional metadata filter
            
        Returns:
            List of relevant documents with scores
        """
        top_k = top_k or settings.TOP_K_RESULTS
        
        # Generate query embedding
        logger.info(f"Retrieving documents for query: '{query[:50]}...'")
        query_embedding = self.embedding_gen.generate_embedding(query)
        
        # Search vector store
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            metadata_filter=metadata_filter
        )
        
        return results
    
    def generate_response(self, query: str, context_docs: List[Dict],
                         system_prompt: str = None) -> str:
        """
        Generate a response using retrieved context and LLM.
        
        Args:
            query: User query
            context_docs: Retrieved context documents
            system_prompt: Optional custom system prompt
            
        Returns:
            Generated response
        """
        # Build context from retrieved documents
        context = "\n\n".join([
            f"Document {i+1} (score: {doc['score']:.3f}):\n{doc['text']}"
            for i, doc in enumerate(context_docs)
        ])
        
        # Default system prompt if not provided
        if not system_prompt:
            system_prompt = """You are a helpful AI assistant. Answer the user's question based on the provided context.
If the context doesn't contain relevant information, say so honestly.
Always cite which document number(s) you're referencing."""
        
        # Create prompt with context
        user_prompt = f"""Context:
{context}

Question: {query}

Please provide a detailed answer based on the context above."""
        
        # Generate response using OpenAI
        try:
            logger.info("Generating response with LLM...")
            response = self.llm_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.TEMPERATURE
            )
            
            answer = response.choices[0].message.content
            logger.info("Response generated successfully")
            return answer
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    def query(self, question: str, top_k: int = None,
             metadata_filter: Dict = None) -> Dict:
        """
        Complete RAG query: retrieve and generate response.
        
        Args:
            question: User question
            top_k: Number of documents to retrieve
            metadata_filter: Optional metadata filter
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(
            query=question,
            top_k=top_k,
            metadata_filter=metadata_filter
        )
        
        if not retrieved_docs:
            return {
                'answer': "I couldn't find any relevant information to answer your question.",
                'sources': [],
                'query': question
            }
        
        # Generate response
        answer = self.generate_response(question, retrieved_docs)
        
        return {
            'answer': answer,
            'sources': retrieved_docs,
            'query': question,
            'num_sources': len(retrieved_docs)
        }
    
    def get_stats(self) -> Dict:
        """Get statistics about the RAG system"""
        return self.vector_store.get_collection_info()