"""
YouTube Podcast Summarizer
Main summarizer class combining transcript extraction and RAG
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from phase1_foundation.rag_pipeline.retriever import RAGRetriever
from phase1_foundation.mini_projects.youtube_summarizer.transcript_extractor import TranscriptExtractor
from shared.utils.logger import logger

class YouTubeSummarizer:
    """
    Summarizes YouTube videos using transcripts and RAG
    """
    
    def __init__(self):
        """Initialize the YouTube summarizer"""
        logger.info("Initializing YouTube Summarizer...")
        
        self.extractor = TranscriptExtractor()
        self.rag = RAGRetriever()
        
        logger.info("YouTube Summarizer initialized")
    
    def summarize_video(self, video_url: str, summary_type: str = 'comprehensive') -> Dict:
        """
        Summarize a YouTube video
        
        Args:
            video_url: YouTube video URL
            summary_type: Type of summary ('brief', 'comprehensive', 'detailed')
            
        Returns:
            Dictionary with summary and metadata
        """
        logger.info(f"Starting summarization for: {video_url}")
        
        # Extract transcript
        transcript_data = self.extractor.get_transcript(video_url)
        
        # Ingest transcript into RAG (with chunking)
        metadata = {
            'video_id': transcript_data['video_id'],
            'type': 'youtube_transcript',
            'duration': transcript_data['duration_seconds']
        }
        
        self.rag.ingest_documents(
            texts=[transcript_data['full_text']],
            metadata=[metadata]
        )
        
        # Generate summary based on type
        if summary_type == 'brief':
            summary = self._generate_brief_summary(transcript_data)
        elif summary_type == 'detailed':
            summary = self._generate_detailed_summary(transcript_data)
        else:  # comprehensive
            summary = self._generate_comprehensive_summary(transcript_data)
        
        result = {
            'video_id': transcript_data['video_id'],
            'video_url': f"https://youtube.com/watch?v={transcript_data['video_id']}",
            'duration': transcript_data['duration_seconds'],
            'summary_type': summary_type,
            'summary': summary,
            'transcript_length': len(transcript_data['full_text']),
            'total_segments': transcript_data['total_segments']
        }
        
        logger.info(f"Summarization complete for {transcript_data['video_id']}")
        
        return result
    
    def _generate_brief_summary(self, transcript_data: Dict) -> str:
        """Generate a brief summary (2-3 paragraphs)"""
        query = "Provide a brief 2-3 paragraph summary of the main topics discussed in this video."
        
        # Retrieve relevant chunks
        docs = self.rag.retrieve(query, top_k=5)
        
        # Generate summary
        system_prompt = """You are a video content summarizer. Create a brief, 
high-level summary of the video content in 2-3 paragraphs. Focus on the main topics 
and key takeaways. Be concise and clear."""
        
        summary = self.rag.generate_response(query, docs, system_prompt)
        return summary
    
    def _generate_comprehensive_summary(self, transcript_data: Dict) -> str:
        """Generate a comprehensive summary with key points"""
        query = "Provide a comprehensive summary including main topics, key points, and important details."
        
        # Retrieve more chunks for comprehensive summary
        docs = self.rag.retrieve(query, top_k=10)
        
        system_prompt = """You are a video content summarizer. Create a comprehensive summary 
that includes:
1. Main topics covered
2. Key points and insights
3. Important details and examples
4. Conclusions or takeaways

Structure the summary with clear sections. Be thorough but organized."""
        
        summary = self.rag.generate_response(query, docs, system_prompt)
        return summary
    
    def _generate_detailed_summary(self, transcript_data: Dict) -> str:
        """Generate a detailed summary with timestamps"""
        query = "Provide a detailed breakdown of the video content with major sections."
        
        docs = self.rag.retrieve(query, top_k=15)
        
        system_prompt = """You are a video content summarizer. Create a detailed summary 
organized by major sections. For each section:
- Describe the main topic
- List key points discussed
- Note important quotes or examples

Make it easy to navigate and understand the video's structure."""
        
        summary = self.rag.generate_response(query, docs, system_prompt)
        return summary
    
    def ask_about_video(self, question: str) -> Dict:
        """
        Ask a question about the most recently processed video
        
        Args:
            question: Question about the video content
            
        Returns:
            Dictionary with answer and sources
        """
        logger.info(f"Answering question: {question[:50]}...")
        
        # Retrieve relevant segments
        docs = self.rag.retrieve(question, top_k=5)
        
        if not docs:
            return {
                'answer': "I don't have enough information to answer that question about the video.",
                'sources': []
            }
        
        # Generate answer
        system_prompt = """You are a helpful assistant answering questions about a YouTube video. 
Answer based on the transcript segments provided. Be specific and cite relevant parts of the video."""
        
        answer = self.rag.generate_response(question, docs, system_prompt)
        
        return {
            'answer': answer,
            'sources': docs,
            'num_sources': len(docs)
        }
    
    def get_key_topics(self, video_url: str, num_topics: int = 5) -> Dict:
        """
        Extract key topics from a video
        
        Args:
            video_url: YouTube video URL
            num_topics: Number of topics to extract
            
        Returns:
            Dictionary with topics and descriptions
        """
        # Get transcript
        transcript_data = self.extractor.get_transcript(video_url)
        
        # Ingest if not already done
        metadata = {'video_id': transcript_data['video_id'], 'type': 'youtube_transcript'}
        self.rag.ingest_documents(texts=[transcript_data['full_text']], metadata=[metadata])
        
        # Query for topics
        query = f"What are the {num_topics} main topics or themes discussed in this video?"
        docs = self.rag.retrieve(query, top_k=10)
        
        system_prompt = f"""Extract the {num_topics} main topics discussed in this video. 
For each topic, provide:
1. Topic name
2. Brief description (1-2 sentences)

Format as a numbered list."""
        
        topics_text = self.rag.generate_response(query, docs, system_prompt)
        
        return {
            'video_id': transcript_data['video_id'],
            'num_topics': num_topics,
            'topics': topics_text
        }