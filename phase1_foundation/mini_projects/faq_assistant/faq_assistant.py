"""
FAQ Assistant
Intelligent Q&A system with conversation memory
"""
import sys
from pathlib import Path
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from phase1_foundation.rag_pipeline.retriever import RAGRetriever
from phase1_foundation.mini_projects.faq_assistant.conversation_manager import ConversationManager
from phase1_foundation.mini_projects.faq_assistant.faq_data import FAQDataManager
from shared.config.settings import settings
from shared.utils.logger import logger

class FAQAssistant:
    """
    FAQ Assistant with RAG and conversation memory
    """
    
    def __init__(self, faq_data_path: str = None):
        """
        Initialize the FAQ Assistant
        
        Args:
            faq_data_path: Path to FAQ data file
        """
        logger.info("Initializing FAQ Assistant...")
        
        # Initialize components
        self.rag = RAGRetriever()
        self.conversation = ConversationManager(max_history=10)
        self.data_manager = FAQDataManager(faq_data_path)
        
        # Load and ingest FAQs
        self._load_knowledge_base()
        
        logger.info("FAQ Assistant initialized successfully")
    
    def _load_knowledge_base(self):
        """Load FAQs into the RAG system"""
        logger.info("Loading FAQ knowledge base...")
        
        # Load FAQs from file
        faqs = self.data_manager.load_faqs()
        
        # Format for ingestion
        texts, metadata = self.data_manager.format_for_ingestion(faqs)
        
        # Ingest into RAG system
        self.rag.ingest_documents(texts=texts, metadata=metadata)
        
        logger.info(f"Knowledge base loaded: {len(faqs)} FAQs")
    
    def ask(self, question: str, include_sources: bool = True) -> Dict:
        """
        Ask a question to the FAQ assistant
        
        Args:
            question: User's question
            include_sources: Whether to include source documents in response
            
        Returns:
            Dictionary with answer, sources, and conversation context
        """
        logger.info(f"Processing question: {question[:50]}...")
        
        # Build context from conversation history
        conversation_context = self.conversation.format_for_context(last_n=3)
        
        # Create enhanced query with context
        if conversation_context:
            enhanced_query = f"{conversation_context}\n\nCurrent question: {question}"
        else:
            enhanced_query = question
        
        # Retrieve relevant FAQs
        retrieved_docs = self.rag.retrieve(
            query=enhanced_query,
            top_k=3,
            metadata_filter={'type': 'faq'}
        )
        
        if not retrieved_docs:
            response = {
                'answer': "I couldn't find relevant information to answer your question. Could you rephrase or ask something else?",
                'sources': [],
                'has_context': False
            }
        else:
            # Generate response with custom system prompt
            system_prompt = """You are a helpful AI teaching assistant for an AI/ML course. 
Answer questions based on the provided FAQ context. Be friendly, clear, and concise.
If the context mentions prerequisites or requirements, list them clearly.
If asked about projects or topics, provide specific details from the FAQs.
Always cite which FAQ(s) you're referencing."""
            
            answer = self.rag.generate_response(
                query=question,
                context_docs=retrieved_docs,
                system_prompt=system_prompt
            )
            
            response = {
                'answer': answer,
                'sources': retrieved_docs if include_sources else [],
                'has_context': True,
                'num_sources': len(retrieved_docs)
            }
        
        # Add to conversation history
        self.conversation.add_turn(
            user_message=question,
            assistant_message=response['answer'],
            sources=response.get('sources', [])
        )
        
        return response
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation.get_history()
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation.clear_history()
        logger.info("Conversation reset")
    
    def get_stats(self) -> Dict:
        """Get assistant statistics"""
        rag_stats = self.rag.get_stats()
        conv_stats = self.conversation.get_summary()
        
        return {
            'rag_stats': rag_stats,
            'conversation_stats': conv_stats
        }