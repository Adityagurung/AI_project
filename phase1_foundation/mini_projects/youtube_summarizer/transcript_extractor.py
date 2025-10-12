"""
YouTube Transcript Extractor
Handles downloading and processing of YouTube transcripts
"""
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from typing import Dict, List, Optional
import re
from shared.utils.logger import logger

class TranscriptExtractor:
    """
    Extracts transcripts from YouTube videos
    """
    
    def __init__(self):
        """Initialize the transcript extractor"""
        logger.info("TranscriptExtractor initialized")
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Args:
            url: YouTube URL
            
        Returns:
            Video ID or None if not found
        """
        # Pattern for YouTube URLs
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # If no pattern matches, assume it's already a video ID
        if len(url) == 11 and ' ' not in url:
            return url
        
        return None
    
    def get_transcript(self, video_url: str, language: str = 'en') -> Dict:
        """
        Get transcript for a YouTube video
        
        Args:
            video_url: YouTube video URL or ID
            language: Preferred language code
            
        Returns:
            Dictionary with transcript data
        """
        video_id = self.extract_video_id(video_url)
        
        if not video_id:
            raise ValueError(f"Could not extract video ID from: {video_url}")
        
        logger.info(f"Fetching transcript for video: {video_id}")
        
        try:
            # Get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=[language]
            )
            
            # Process transcript
            full_text = ' '.join([entry['text'] for entry in transcript_list])
            
            result = {
                'video_id': video_id,
                'language': language,
                'transcript_entries': transcript_list,
                'full_text': full_text,
                'duration_seconds': transcript_list[-1]['start'] + transcript_list[-1]['duration'] if transcript_list else 0,
                'total_segments': len(transcript_list)
            }
            
            logger.info(f"Transcript extracted: {len(transcript_list)} segments, "
                       f"{len(full_text)} characters")
            
            return result
            
        except TranscriptsDisabled:
            raise Exception(f"Transcripts are disabled for video: {video_id}")
        except NoTranscriptFound:
            raise Exception(f"No transcript found for video: {video_id} in language: {language}")
        except Exception as e:
            logger.error(f"Error fetching transcript: {str(e)}")
            raise
    
    def get_transcript_with_timestamps(self, video_url: str) -> List[Dict]:
        """
        Get transcript with timestamp information
        
        Args:
            video_url: YouTube video URL or ID
            
        Returns:
            List of transcript segments with timestamps
        """
        video_id = self.extract_video_id(video_url)
        
        if not video_id:
            raise ValueError(f"Could not extract video ID from: {video_url}")
        
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Format timestamps
            formatted_segments = []
            for entry in transcript_list:
                formatted_segments.append({
                    'timestamp': self._format_timestamp(entry['start']),
                    'start_seconds': entry['start'],
                    'duration': entry['duration'],
                    'text': entry['text']
                })
            
            return formatted_segments
            
        except Exception as e:
            logger.error(f"Error fetching timestamped transcript: {str(e)}")
            raise
    
    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """
        Format seconds as HH:MM:SS
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted timestamp string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"