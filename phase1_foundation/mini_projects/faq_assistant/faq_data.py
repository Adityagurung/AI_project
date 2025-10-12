"""
FAQ Data Management
Handles loading and processing of FAQ datasets
"""
from pathlib import Path
from typing import List, Dict
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.utils.logger import logger

class FAQDataManager:
    """
    Manages FAQ data loading and preprocessing
    """
    
    def __init__(self, data_path: str = None):
        """
        Initialize the FAQ data manager
        
        Args:
            data_path: Path to FAQ text file
        """
        if data_path is None:
            # Default path to student FAQs
            self.data_path = Path(__file__).parent.parent.parent / "data" / "faqs" / "student_faqs.txt"
        else:
            self.data_path = Path(data_path)
        
        logger.info(f"FAQDataManager initialized with data_path: {self.data_path}")
    
    def load_faqs(self) -> List[Dict[str, str]]:
        """
        Load FAQs from text file
        
        Returns:
            List of dictionaries with 'question' and 'answer' keys
        """
        if not self.data_path.exists():
            logger.error(f"FAQ file not found: {self.data_path}")
            raise FileNotFoundError(f"FAQ file not found: {self.data_path}")
        
        faqs = []
        
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by double newlines to separate FAQ pairs
            faq_blocks = content.strip().split('\n\n')
            
            for block in faq_blocks:
                lines = block.strip().split('\n')
                
                # Look for Question: and Answer: patterns
                question = None
                answer = None
                
                for line in lines:
                    if line.startswith('Question:'):
                        question = line.replace('Question:', '').strip()
                    elif line.startswith('Answer:'):
                        answer = line.replace('Answer:', '').strip()
                
                if question and answer:
                    faqs.append({
                        'question': question,
                        'answer': answer,
                        'metadata': {
                            'source': 'student_faqs',
                            'type': 'faq'
                        }
                    })
            
            logger.info(f"Loaded {len(faqs)} FAQs from {self.data_path.name}")
            return faqs
            
        except Exception as e:
            logger.error(f"Error loading FAQs: {str(e)}")
            raise
    
    def format_for_ingestion(self, faqs: List[Dict[str, str]]) -> tuple:
        """
        Format FAQs for RAG pipeline ingestion
        
        Args:
            faqs: List of FAQ dictionaries
            
        Returns:
            Tuple of (texts, metadata) for ingestion
        """
        texts = []
        metadata_list = []
        
        for faq in faqs:
            # Combine question and answer for better retrieval
            combined_text = f"Question: {faq['question']}\n\nAnswer: {faq['answer']}"
            texts.append(combined_text)
            
            # Add metadata
            metadata_list.append({
                'question': faq['question'],
                'source': faq.get('metadata', {}).get('source', 'unknown'),
                'type': 'faq'
            })
        
        logger.info(f"Formatted {len(texts)} FAQs for ingestion")
        return texts, metadata_list