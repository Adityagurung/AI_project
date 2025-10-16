"""
Unified Assistant Manager
Orchestrates multiple AI assistants into a single interface

This brings together:
1. FAQ Assistant - Answers course-related questions
2. YouTube Summarizer - Summarizes video content  
3. Docs Assistant - Searches internal documents

Think of this as a switchboard operator that routes your
question to the right specialist assistant.
"""
import sys
from pathlib import Path
from typing import Dict, Optional, List
from enum import Enum

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from phase1_foundation.mini_projects.faq_assistant.faq_assistant import FAQAssistant
from phase1_foundation.mini_projects.youtube_summarizer.mock_youtube_summarizer import MockYouTubeSummarizer
from phase1_foundation.mini_projects.docs_assistant.docs_assistant import DocsAssistant
from shared.utils.logger import logger


class AssistantType(Enum):
    """Types of available assistants"""
    FAQ = "faq"
    YOUTUBE = "youtube"
    DOCS = "docs"


class UnifiedAssistantManager:
    """
    Unified manager for all AI assistants
    
    This class provides a single interface to interact with
    all three specialized assistants. You can:
    - Switch between assistants
    - Use each assistant's capabilities
    - Get combined statistics
    """
    
    def __init__(self):
        """
        Initialize the unified assistant manager
        
        This creates all three assistants and makes them ready to use.
        """
        logger.info("Initializing Unified Assistant Manager...")
        
        # Initialize all three assistants
        self.faq_assistant = None
        self.youtube_summarizer = None
        self.docs_assistant = None
        
        # Track which assistant is currently active
        self.current_assistant = None
        
        # Initialize assistants
        self._initialize_assistants()
        
        logger.info("Unified Assistant Manager initialized successfully")
    
    def _initialize_assistants(self):
        """
        Initialize all three specialized assistants
        
        We do this separately so we can handle errors for each one.
        """
        # Initialize FAQ Assistant
        try:
            logger.info("Initializing FAQ Assistant...")
            self.faq_assistant = FAQAssistant()
            logger.info("FAQ Assistant ready")
        except Exception as e:
            logger.error(f"Failed to initialize FAQ Assistant: {e}")
            self.faq_assistant = None
        
        # Initialize YouTube Summarizer (mock version)
        try:
            logger.info("Initializing YouTube Summarizer...")
            self.youtube_summarizer = MockYouTubeSummarizer()
            logger.info("YouTube Summarizer ready")
        except Exception as e:
            logger.error(f"Failed to initialize YouTube Summarizer: {e}")
            self.youtube_summarizer = None
        
        # Initialize Docs Assistant
        try:
            logger.info("Initializing Docs Assistant...")
            self.docs_assistant = DocsAssistant()
            # Load documents automatically
            result = self.docs_assistant.load_documents()
            logger.info(f"Docs Assistant ready - loaded {result['loaded']} documents")
        except Exception as e:
            logger.error(f"Failed to initialize Docs Assistant: {e}")
            self.docs_assistant = None
    
    def switch_assistant(self, assistant_type: str) -> Dict:
        """
        Switch to a different assistant
        
        Args:
            assistant_type: Type of assistant ('faq', 'youtube', 'docs')
        
        Returns:
            Dictionary with switch status and info
        """
        # Normalize input
        assistant_type = assistant_type.lower().strip()
        
        # Map to enum
        type_map = {
            'faq': AssistantType.FAQ,
            'youtube': AssistantType.YOUTUBE,
            'docs': AssistantType.DOCS,
            'document': AssistantType.DOCS,
            'documents': AssistantType.DOCS,
            'video': AssistantType.YOUTUBE
        }
        
        if assistant_type not in type_map:
            return {
                'success': False,
                'message': f"Unknown assistant type: {assistant_type}",
                'available': list(type_map.keys())
            }
        
        target_type = type_map[assistant_type]
        
        # Check if assistant is available
        assistant_map = {
            AssistantType.FAQ: self.faq_assistant,
            AssistantType.YOUTUBE: self.youtube_summarizer,
            AssistantType.DOCS: self.docs_assistant
        }
        
        if assistant_map[target_type] is None:
            return {
                'success': False,
                'message': f"{target_type.value} assistant is not available"
            }
        
        # Switch to the new assistant
        old_assistant = self.current_assistant
        self.current_assistant = target_type
        
        logger.info(f"Switched from {old_assistant} to {target_type.value}")
        
        return {
            'success': True,
            'previous': old_assistant.value if old_assistant else None,
            'current': target_type.value,
            'message': f"Switched to {target_type.value} assistant"
        }
    
    def ask_faq(self, question: str) -> Dict:
        """
        Ask a question to the FAQ Assistant
        
        Args:
            question: User's question
        
        Returns:
            Response from FAQ Assistant
        """
        if self.faq_assistant is None:
            return {
                'answer': "FAQ Assistant is not available",
                'sources': [],
                'error': True
            }
        
        logger.info(f"FAQ question: {question[:50]}...")
        response = self.faq_assistant.ask(question)
        response['assistant_type'] = 'faq'
        return response
    
    def summarize_video(self, video_key: str, summary_type: str = 'brief') -> Dict:
        """
        Summarize a video using YouTube Summarizer
        
        Args:
            video_key: Video identifier (for mock: 'procrastination' or 'ai_basics')
            summary_type: Type of summary ('brief', 'comprehensive', 'detailed')
        
        Returns:
            Summary results
        """
        if self.youtube_summarizer is None:
            return {
                'summary': "YouTube Summarizer is not available",
                'error': True
            }
        
        logger.info(f"Summarizing video: {video_key}")
        
        try:
            result = self.youtube_summarizer.summarize_video(video_key, summary_type)
            result['assistant_type'] = 'youtube'
            return result
        except Exception as e:
            return {
                'summary': f"Error summarizing video: {str(e)}",
                'error': True
            }
    
    def ask_about_video(self, question: str) -> Dict:
        """
        Ask a question about the most recently summarized video
        
        Args:
            question: Question about the video
        
        Returns:
            Answer from YouTube Summarizer
        """
        if self.youtube_summarizer is None:
            return {
                'answer': "YouTube Summarizer is not available",
                'error': True
            }
        
        logger.info(f"Video question: {question[:50]}...")
        response = self.youtube_summarizer.ask_about_video(question)
        response['assistant_type'] = 'youtube'
        return response
    
    def search_documents(self, query: str, top_k: int = 3) -> Dict:
        """
        Search internal documents
        
        Args:
            query: Search query
            top_k: Number of results
        
        Returns:
            Search results
        """
        if self.docs_assistant is None:
            return {
                'answer': "Docs Assistant is not available",
                'sources': [],
                'error': True
            }
        
        logger.info(f"Document search: {query[:50]}...")
        response = self.docs_assistant.ask(query, top_k=top_k)
        response['assistant_type'] = 'docs'
        return response
    
    def summarize_document(self, filename: str) -> Dict:
        """
        Summarize a specific document
        
        Args:
            filename: Name of document to summarize
        
        Returns:
            Document summary
        """
        if self.docs_assistant is None:
            return {
                'summary': "Docs Assistant is not available",
                'error': True
            }
        
        logger.info(f"Summarizing document: {filename}")
        result = self.docs_assistant.summarize_document(filename)
        result['assistant_type'] = 'docs'
        return result
    
    def list_available_documents(self) -> List[Dict]:
        """
        List all available documents
        
        Returns:
            List of document metadata
        """
        if self.docs_assistant is None:
            return []
        
        return self.docs_assistant.list_documents()
    
    def list_available_videos(self):
        """
        List available mock videos
        
        Shows what videos the YouTube Summarizer can process
        """
        if self.youtube_summarizer is None:
            print("YouTube Summarizer is not available")
            return
        
        self.youtube_summarizer.list_available_videos()
    
    def auto_route(self, query: str) -> Dict:
        """
        Automatically route query to the most appropriate assistant
        
        This is smart routing - it analyzes the query and picks
        the best assistant to handle it.
        
        Args:
            query: User's query
        
        Returns:
            Response from the selected assistant
        """
        query_lower = query.lower()
        
        # Keywords for each assistant
        faq_keywords = ['course', 'prerequisite', 'how long', 'cost', 'certification', 
                       'gpu', 'requirement', 'tool', 'project']
        youtube_keywords = ['video', 'summarize', 'youtube', 'watch', 'procrastination',
                          'talk', 'ai basics']
        docs_keywords = ['document', 'rag', 'python', 'best practice', 'phase',
                        'tip', 'project info']
        
        # Count keyword matches
        faq_score = sum(1 for keyword in faq_keywords if keyword in query_lower)
        youtube_score = sum(1 for keyword in youtube_keywords if keyword in query_lower)
        docs_score = sum(1 for keyword in docs_keywords if keyword in query_lower)
        
        # Route to highest scoring assistant
        if faq_score > youtube_score and faq_score > docs_score:
            logger.info(f"Auto-routing to FAQ Assistant (score: {faq_score})")
            return self.ask_faq(query)
        elif youtube_score > faq_score and youtube_score > docs_score:
            logger.info(f"Auto-routing to YouTube Summarizer (score: {youtube_score})")
            # For YouTube, we need a video key, so return instruction
            return {
                'answer': "To summarize a video, use: summarize_video('procrastination') or summarize_video('ai_basics')",
                'assistant_type': 'youtube',
                'auto_routed': True
            }
        else:
            # Default to docs for general queries
            logger.info(f"Auto-routing to Docs Assistant (score: {docs_score})")
            return self.search_documents(query)
    
    def get_status(self) -> Dict:
        """
        Get status of all assistants
        
        Returns:
            Status dictionary with info about each assistant
        """
        return {
            'faq_assistant': {
                'available': self.faq_assistant is not None,
                'status': 'ready' if self.faq_assistant else 'unavailable'
            },
            'youtube_summarizer': {
                'available': self.youtube_summarizer is not None,
                'status': 'ready' if self.youtube_summarizer else 'unavailable'
            },
            'docs_assistant': {
                'available': self.docs_assistant is not None,
                'status': 'ready' if self.docs_assistant else 'unavailable',
                'documents_loaded': len(self.docs_assistant.documents) if self.docs_assistant else 0
            },
            'current_assistant': self.current_assistant.value if self.current_assistant else None
        }
    
    def get_combined_stats(self) -> Dict:
        """
        Get combined statistics from all assistants
        
        Returns:
            Dictionary with stats from each assistant
        """
        stats = {
            'manager': {
                'assistants_available': sum([
                    self.faq_assistant is not None,
                    self.youtube_summarizer is not None,
                    self.docs_assistant is not None
                ]),
                'current_assistant': self.current_assistant.value if self.current_assistant else None
            }
        }
        
        # FAQ stats
        if self.faq_assistant:
            try:
                faq_stats = self.faq_assistant.get_stats()
                stats['faq'] = faq_stats
            except:
                stats['faq'] = {'error': 'Unable to get stats'}
        
        # Docs stats
        if self.docs_assistant:
            try:
                docs_stats = self.docs_assistant.get_stats()
                stats['docs'] = docs_stats
            except:
                stats['docs'] = {'error': 'Unable to get stats'}
        
        return stats
    
    def help(self) -> str:
        """
        Get help text explaining available commands
        
        Returns:
            Help text string
        """
        help_text = """
🤖 UNIFIED AI ASSISTANT - HELP
============================================================

AVAILABLE ASSISTANTS:
1. FAQ Assistant      - Answers course-related questions
2. YouTube Summarizer - Summarizes video content (mock data)
3. Docs Assistant     - Searches internal documents

MAIN COMMANDS:
- ask_faq("question")                    Ask FAQ Assistant
- search_documents("query")              Search documents
- summarize_video("video_key")           Summarize a video
- ask_about_video("question")            Ask about last video

UTILITY COMMANDS:
- switch_assistant("type")               Switch assistants
- list_available_documents()             Show documents
- list_available_videos()                Show videos
- get_status()                           Check status
- get_combined_stats()                   Show statistics
- auto_route("query")                    Smart routing

TIPS:
- Use auto_route() for automatic assistant selection
- Each assistant maintains its own context
- Switch between assistants as needed
============================================================
        """
        return help_text