"""
Internal Docs Assistant
Intelligent document search and Q&A system

This assistant:
1. Loads documents using DocumentLoader
2. Ingests them into the RAG system
3. Answers questions based on document content
4. Cites sources (which document the answer came from)
5. Can filter by document type or name
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from phase1_foundation.rag_pipeline.retriever import RAGRetriever
from phase1_foundation.mini_projects.docs_assistant.document_loader import DocumentLoader
from shared.config.settings import settings
from shared.utils.logger import logger


class DocsAssistant:
    """
    Intelligent assistant for internal documents
    
    Think of this as your personal librarian who has read all your
    documents and can answer questions about them instantly.
    """
    
    def __init__(self, documents_dir: str = None):
        """
        Initialize the Docs Assistant
        
        Args:
            documents_dir: Path to documents folder (optional)
        """
        logger.info("Initializing Docs Assistant...")
        
        # Initialize components
        self.rag = RAGRetriever()
        self.loader = DocumentLoader(documents_dir)
        
        # Store loaded documents for reference
        self.documents = []
        self.document_index = {}  # Map document names to their content
        
        logger.info("Docs Assistant initialized")
    
    def load_documents(self) -> Dict:
        """
        Load all documents from the documents directory
        
        This reads all your documents and prepares them for searching.
        
        Returns:
            Dictionary with loading statistics
        """
        logger.info("Loading documents...")
        
        # Load all documents
        self.documents = self.loader.load_all_documents()
        
        if not self.documents:
            logger.warning("No documents found to load")
            return {
                'loaded': 0,
                'failed': 0,
                'summary': {}
            }
        
        # Prepare texts and metadata for RAG ingestion
        texts = []
        metadata_list = []
        
        for doc in self.documents:
            # Extract content and metadata
            content = doc['content']
            meta = doc['metadata']
            
            # Add to texts list
            texts.append(content)
            
            # Prepare metadata for RAG system
            # This helps us filter and cite sources later
            metadata_list.append({
                'source': meta['filename'],
                'type': meta['type'],
                'extension': meta['extension'],
                'size': meta['size_bytes'],
                'modified': meta['modified']
            })
            
            # Build index for quick lookup
            self.document_index[meta['filename']] = {
                'content': content,
                'metadata': meta
            }
        
        # Ingest all documents into RAG system
        logger.info(f"Ingesting {len(texts)} documents into RAG system...")
        self.rag.ingest_documents(texts=texts, metadata=metadata_list)
        
        # Get summary statistics
        summary = self.loader.get_document_summary(self.documents)
        
        logger.info(f"Successfully loaded {len(self.documents)} documents")
        
        return {
            'loaded': len(self.documents),
            'failed': 0,
            'summary': summary
        }
    
    def search(self, query: str, top_k: int = 3, 
               doc_type: Optional[str] = None) -> List[Dict]:
        """
        Search documents for relevant information
        
        This is like using Ctrl+F but smarter - it understands meaning,
        not just exact word matches.
        
        Args:
            query: Search query or question
            top_k: Number of results to return (default: 3)
            doc_type: Filter by document type (e.g., 'text', 'pdf')
        
        Returns:
            List of relevant document chunks with metadata
        """
        logger.info(f"Searching for: {query[:50]}...")
        
        # Build metadata filter if doc_type specified
        metadata_filter = None
        if doc_type:
            metadata_filter = {'type': doc_type}
            logger.info(f"Filtering by type: {doc_type}")
        
        # Retrieve relevant chunks from RAG system
        results = self.rag.retrieve(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter
        )
        
        logger.info(f"Found {len(results)} relevant chunks")
        
        return results
    
    def ask(self, question: str, top_k: int = 5, 
            include_sources: bool = True) -> Dict:
        """
        Ask a question about your documents
        
        This is the main interface - ask anything about your documents
        and get an answer with source citations.
        
        Args:
            question: Your question
            top_k: How many document chunks to consider
            include_sources: Whether to include source documents in response
        
        Returns:
            Dictionary with answer, sources, and metadata
        """
        logger.info(f"Processing question: {question[:50]}...")
        
        if not self.documents:
            return {
                'answer': "No documents loaded. Please load documents first using load_documents().",
                'sources': [],
                'has_documents': False
            }
        
        # Search for relevant information
        relevant_docs = self.search(question, top_k=top_k)
        
        if not relevant_docs:
            return {
                'answer': "I couldn't find relevant information in the documents to answer your question.",
                'sources': [],
                'has_documents': True
            }
        
        # Generate answer using RAG
        system_prompt = """You are a helpful assistant that answers questions based on 
internal documents. Always cite which document(s) you're using to answer. Be accurate 
and specific. If the documents don't contain enough information to answer fully, 
say so clearly."""
        
        answer = self.rag.generate_response(
            query=question,
            context_docs=relevant_docs,
            system_prompt=system_prompt
        )
        
        # Extract unique source documents
        sources = []
        seen_sources = set()
        
        for doc in relevant_docs:
            source_name = doc.get('metadata', {}).get('source', 'Unknown')
            if source_name not in seen_sources:
                sources.append({
                    'filename': source_name,
                    'type': doc.get('metadata', {}).get('type', 'unknown'),
                    'relevance_score': doc.get('score', 0.0)
                })
                seen_sources.add(source_name)
        
        result = {
            'answer': answer,
            'sources': sources if include_sources else [],
            'num_sources': len(sources),
            'has_documents': True
        }
        
        logger.info(f"Answer generated using {len(sources)} source document(s)")
        
        return result
    
    def summarize_document(self, filename: str) -> Dict:
        """
        Generate a summary of a specific document
        
        Args:
            filename: Name of the document to summarize
        
        Returns:
            Dictionary with summary and metadata
        """
        logger.info(f"Summarizing document: {filename}")
        
        # Check if document exists
        if filename not in self.document_index:
            available = list(self.document_index.keys())
            return {
                'summary': f"Document '{filename}' not found. Available documents: {available}",
                'success': False
            }
        
        # Get document content
        doc_info = self.document_index[filename]
        content = doc_info['content']
        
        # Create query for summarization
        query = f"Provide a comprehensive summary of the document '{filename}'"
        
        # Search for relevant parts (gets chunks from this specific document)
        relevant_docs = self.rag.retrieve(
            query=query,
            top_k=10,
            metadata_filter={'source': filename}
        )
        
        # Generate summary
        system_prompt = f"""You are summarizing the document '{filename}'. 
Provide a clear, comprehensive summary that covers:
1. Main topic/purpose
2. Key points
3. Important details
Keep it concise but informative."""
        
        summary = self.rag.generate_response(
            query=query,
            context_docs=relevant_docs,
            system_prompt=system_prompt
        )
        
        return {
            'summary': summary,
            'filename': filename,
            'type': doc_info['metadata']['type'],
            'size': doc_info['metadata']['size_bytes'],
            'success': True
        }
    
    def list_documents(self) -> List[Dict]:
        """
        Get list of all loaded documents
        
        Returns:
            List of document metadata dictionaries
        """
        return [
            {
                'filename': doc['metadata']['filename'],
                'type': doc['metadata']['type'],
                'size_bytes': doc['metadata']['size_bytes'],
                'modified': doc['metadata']['modified']
            }
            for doc in self.documents
        ]
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the assistant
        
        Returns:
            Dictionary with statistics
        """
        rag_stats = self.rag.get_stats()
        doc_summary = self.loader.get_document_summary(self.documents)
        
        return {
            'documents_loaded': len(self.documents),
            'document_summary': doc_summary,
            'rag_stats': rag_stats,
            'available_documents': list(self.document_index.keys())
        }