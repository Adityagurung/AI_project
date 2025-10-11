"""
Document processing module for chunking and preparing text for embedding.
Handles various file formats and implements intelligent chunking strategies.
"""
from typing import List, Dict
from pathlib import Path
import tiktoken
from shared.config.settings import settings
from shared.utils.logger import logger

class DocumentProcessor:
    """
    Processes documents by chunking them into smaller, manageable pieces.
    """
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Maximum size of each chunk in tokens
            chunk_overlap: Number of tokens to overlap between chunks
        """
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        
        # Initialize tokenizer for accurate token counting
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        
        logger.info(f"DocumentProcessor initialized with chunk_size={self.chunk_size}, "
                   f"overlap={self.chunk_overlap}")
    
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text.
        
        Args:
            text: Input text
            
        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))
    
    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of dictionaries containing chunk text and metadata
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for chunking")
            return []
        
        # Split text into sentences (simple split on periods)
        sentences = text.replace('\n', ' ').split('. ')
        
        chunks = []
        current_chunk = []
        current_token_count = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Add period back if it was removed
            if not sentence.endswith('.'):
                sentence += '.'
            
            sentence_tokens = self.count_tokens(sentence)
            
            # If adding this sentence exceeds chunk size, save current chunk
            if current_token_count + sentence_tokens > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'text': chunk_text,
                    'token_count': current_token_count,
                    'metadata': metadata or {}
                })
                
                # Start new chunk with overlap
                overlap_text = ' '.join(current_chunk[-2:])  # Last 2 sentences for context
                current_chunk = [overlap_text, sentence] if overlap_text else [sentence]
                current_token_count = self.count_tokens(' '.join(current_chunk))
            else:
                current_chunk.append(sentence)
                current_token_count += sentence_tokens
        
        # Add the last chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'token_count': current_token_count,
                'metadata': metadata or {}
            })
        
        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks
    
    def process_file(self, file_path: str) -> List[Dict]:
        """
        Process a file and return chunks.
        
        Args:
            file_path: Path to the file
            
        Returns:
            List of text chunks with metadata
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read file content based on extension
        if file_path.suffix == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        # Create metadata
        metadata = {
            'source': str(file_path),
            'filename': file_path.name,
            'file_type': file_path.suffix
        }
        
        # Chunk the content
        chunks = self.chunk_text(content, metadata)
        
        logger.info(f"Processed file: {file_path.name} -> {len(chunks)} chunks")
        return chunks