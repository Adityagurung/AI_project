"""
Conversation Manager
Handles conversation history and context management
"""
from typing import List, Dict
from datetime import datetime
from shared.utils.logger import logger

class ConversationManager:
    """
    Manages conversation history for the FAQ assistant
    """
    
    def __init__(self, max_history: int = 10):
        """
        Initialize conversation manager
        
        Args:
            max_history: Maximum number of conversation turns to keep
        """
        self.max_history = max_history
        self.history: List[Dict] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logger.info(f"ConversationManager initialized (session: {self.session_id})")
    
    def add_turn(self, user_message: str, assistant_message: str, 
                 sources: List[Dict] = None):
        """
        Add a conversation turn to history
        
        Args:
            user_message: User's question
            assistant_message: Assistant's response
            sources: Optional list of source documents used
        """
        turn = {
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'assistant': assistant_message,
            'sources': sources or []
        }
        
        self.history.append(turn)
        
        # Keep only last max_history turns
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        logger.debug(f"Added conversation turn (total: {len(self.history)})")
    
    def get_history(self, last_n: int = None) -> List[Dict]:
        """
        Get conversation history
        
        Args:
            last_n: Number of recent turns to retrieve (None for all)
            
        Returns:
            List of conversation turns
        """
        if last_n is None:
            return self.history
        return self.history[-last_n:]
    
    def format_for_context(self, last_n: int = 3) -> str:
        """
        Format conversation history as context string
        
        Args:
            last_n: Number of recent turns to include
            
        Returns:
            Formatted conversation history
        """
        recent_history = self.get_history(last_n)
        
        if not recent_history:
            return ""
        
        context_parts = ["Previous conversation:"]
        
        for i, turn in enumerate(recent_history, 1):
            context_parts.append(f"\nTurn {i}:")
            context_parts.append(f"User: {turn['user']}")
            context_parts.append(f"Assistant: {turn['assistant'][:200]}...")  # Truncate long answers
        
        return "\n".join(context_parts)
    
    def clear_history(self):
        """Clear conversation history"""
        self.history = []
        logger.info("Conversation history cleared")
    
    def get_summary(self) -> Dict:
        """
        Get conversation summary statistics
        
        Returns:
            Dictionary with summary information
        """
        return {
            'session_id': self.session_id,
            'total_turns': len(self.history),
            'first_message': self.history[0]['timestamp'] if self.history else None,
            'last_message': self.history[-1]['timestamp'] if self.history else None
        }