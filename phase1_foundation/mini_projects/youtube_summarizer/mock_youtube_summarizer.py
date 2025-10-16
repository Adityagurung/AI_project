"""
Mock YouTube Summarizer - For Learning When YouTube API is Blocked
Uses sample transcript data to demonstrate functionality
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from phase1_foundation.rag_pipeline.retriever import RAGRetriever
from shared.utils.logger import logger

class MockYouTubeSummarizer:
    """
    Mock YouTube Summarizer using sample transcripts
    """
    
    # Sample transcripts for different topics
    SAMPLE_TRANSCRIPTS = {
        "procrastination": {
            'video_id': 'mock_procrastination',
            'title': 'Inside the Mind of a Master Procrastinator',
            'duration': 840,
            'transcript': """
            So in college, I was a government major, which means I had to write a lot of papers. 
            Now when a normal student writes a paper, they might spread the work out a little like this. 
            So you know, you get started maybe a little slowly, but you get enough done in the first week 
            that with some heavier days later on, everything gets done, things stay civil.
            
            And I would want to do that like that. That would be the plan. I would have it all ready to go, 
            but then actually the paper would come along, and then I would kind of do this. And that would 
            happen every single paper. But then came my 90-page senior thesis, a paper you're supposed to 
            spend a year on. I knew for a paper like that, my normal work flow was not an option, it was 
            way too big a project. So I planned things out and I decided I kind of had to go something like 
            this. This is how the year would go.
            
            So I'd start off light and I'd bump it up in the middle months, and then at the end I would 
            kick it up into high gear just like a little staircase. How hard could it be to walk up the 
            stairs? No big deal, right? But then the funniest thing happened. Those first few months, 
            they came and went, and I couldn't quite do stuff. So we had an awesome new revised plan. 
            And then those middle months actually went by, and I didn't really write words, and so we 
            were here. And then two months turned into one month, which turned into two weeks.
            
            And one day I woke up with three days until the deadline, still not having written a word, 
            and so I did the only thing I could. I wrote 90 pages over 72 hours, pulling not one but 
            two all-nighters, humans are not supposed to pull two all-nighters. Sprinted across campus, 
            dove in slow motion and got it in just at the deadline.
            
            I thought that was the end of everything. But a week later I get a call and it's the school. 
            And they say, "Is this Tim Urban?" And I say, "Yeah." And they say, "We need to talk about 
            your thesis." And I say, "OK." And they say, "It's the best one we've ever seen."
            
            That did not happen. It was a very, very bad thesis. I just wanted to enjoy that one moment 
            when all of you thought, "This guy is amazing!" No, no, it was very, very bad.
            
            Anyway, today I'm a writer-blogger guy. I write the blog Wait But Why. And a couple of years 
            ago I decided to write about procrastination. My behavior has always perplexed the non-procrastinators 
            around me, and I wanted to explain to the non-procrastinators of the world what goes on in the 
            heads of procrastinators and why we are the way we are.
            
            Now I had a hypothesis that the brains of procrastinators were actually different than the brains 
            of other people. And to test this, I found an MRI lab that actually let me scan both my brain and 
            the brain of a proven non-procrastinator, so I could compare them. I actually brought them here to 
            show you today. I want you to take a look carefully to see if you can notice a difference.
            
            I know that both of these brains look identical, but I assure you they're not. There is a 
            difference. Both brains have a Rational Decision-Maker in them, but the procrastinator's brain 
            also has an Instant Gratification Monkey. Now what does this mean for the procrastinator?
            """
        },
        
        "ai_basics": {
            'video_id': 'mock_ai_basics',
            'title': 'Introduction to Artificial Intelligence',
            'duration': 600,
            'transcript': """
            Welcome to this introduction to artificial intelligence. Today we're going to explore what AI is, 
            how it works, and why it matters for our future.
            
            Artificial Intelligence, or AI, refers to computer systems that can perform tasks that typically 
            require human intelligence. These tasks include visual perception, speech recognition, 
            decision-making, and language translation.
            
            There are two main categories of AI. Narrow AI, also called weak AI, is designed to perform 
            specific tasks. Examples include voice assistants like Siri or Alexa, recommendation systems 
            on Netflix, or facial recognition software. This is the type of AI we interact with every day.
            
            General AI, also called strong AI or AGI, refers to AI systems that would have human-like 
            cognitive abilities across a wide range of tasks. This type doesn't exist yet and remains 
            a goal for future research.
            
            Machine learning is a key approach to building AI systems. Instead of explicitly programming 
            every rule, we train systems on large amounts of data. The system learns patterns from the 
            data and can then make predictions or decisions on new, unseen data.
            
            Deep learning, a subset of machine learning, uses neural networks with many layers to process 
            information. These have been particularly successful in areas like image recognition and 
            natural language processing.
            
            AI is transforming many industries. In healthcare, AI helps diagnose diseases and discover 
            new drugs. In transportation, self-driving cars use AI to navigate roads. In finance, AI 
            detects fraud and makes trading decisions.
            
            However, AI also raises important ethical questions. We need to address issues of bias in 
            AI systems, privacy concerns with data collection, and the impact on employment as automation 
            increases. It's crucial that we develop AI responsibly and ensure its benefits are widely shared.
            
            The future of AI is exciting but uncertain. As researchers continue to push boundaries, we'll 
            likely see AI systems that are more capable, more general, and more integrated into our daily 
            lives. Understanding AI basics is important for everyone as we navigate this technological revolution.
            """
        }
    }
    
    def __init__(self):
        """Initialize mock summarizer"""
        logger.info("Initializing Mock YouTube Summarizer...")
        self.rag = RAGRetriever()
        self.current_video = None
        logger.info("Mock YouTube Summarizer initialized")
    
    def list_available_videos(self):
        """Show available mock videos"""
        print("\n📹 Available Mock Videos:")
        print("="*60)
        for key, data in self.SAMPLE_TRANSCRIPTS.items():
            print(f"\nID: {key}")
            print(f"Title: {data['title']}")
            print(f"Duration: {data['duration']} seconds ({data['duration']//60} min)")
        print("\n" + "="*60)
    
    def summarize_video(self, video_key: str, summary_type: str = 'brief') -> dict:
        """
        Summarize a mock video
        
        Args:
            video_key: Key from SAMPLE_TRANSCRIPTS (e.g., 'procrastination', 'ai_basics')
            summary_type: Type of summary
        
        Returns:
            Dictionary with summary results
        """
        if video_key not in self.SAMPLE_TRANSCRIPTS:
            raise ValueError(f"Unknown video key: {video_key}. Use list_available_videos() to see options.")
        
        video_data = self.SAMPLE_TRANSCRIPTS[video_key]
        self.current_video = video_key
        
        logger.info(f"Summarizing mock video: {video_data['title']}")
        
        # Ingest transcript
        metadata = {
            'video_id': video_data['video_id'],
            'type': 'youtube_transcript',
            'title': video_data['title']
        }
        
        self.rag.ingest_documents(
            texts=[video_data['transcript']],
            metadata=[metadata]
        )
        
        # Generate summary based on type
        if summary_type == 'brief':
            query = "Provide a brief 2-3 paragraph summary of the main topics."
        elif summary_type == 'detailed':
            query = "Provide a detailed summary with key points and examples."
        else:
            query = "Provide a comprehensive summary of all main topics and insights."
        
        docs = self.rag.retrieve(query, top_k=5)
        
        system_prompt = """You are a video content summarizer. Create a clear, 
well-structured summary of the video content based on the transcript provided."""
        
        summary = self.rag.generate_response(query, docs, system_prompt)
        
        result = {
            'video_id': video_data['video_id'],
            'title': video_data['title'],
            'duration': video_data['duration'],
            'summary_type': summary_type,
            'summary': summary,
            'transcript_length': len(video_data['transcript'])
        }
        
        return result
    
    def ask_about_video(self, question: str) -> dict:
        """
        Ask a question about the currently loaded video
        
        Args:
            question: Question about the video
            
        Returns:
            Dictionary with answer
        """
        if not self.current_video:
            return {
                'answer': "Please summarize a video first before asking questions.",
                'sources': []
            }
        
        docs = self.rag.retrieve(question, top_k=3)
        
        system_prompt = """You are answering questions about a video. 
Answer based on the transcript provided. Be specific and helpful."""
        
        answer = self.rag.generate_response(question, docs, system_prompt)
        
        return {
            'answer': answer,
            'sources': docs
        }


def demo():
    """Demonstration of mock YouTube summarizer"""
    print("\n" + "="*60)
    print("🎬 MOCK YOUTUBE SUMMARIZER DEMO")
    print("="*60)
    print("\n⚠️  Using mock data because YouTube API is rate-limited")
    print("   This demonstrates the same functionality!")
    
    # Initialize
    summarizer = MockYouTubeSummarizer()
    
    # Show available videos
    summarizer.list_available_videos()
    
    # Summarize procrastination video
    print("\n📊 Summarizing 'Procrastination' video...")
    print("="*60)
    
    result = summarizer.summarize_video('procrastination', 'brief')
    
    print(f"\n📹 Title: {result['title']}")
    print(f"⏱️  Duration: {result['duration']} seconds")
    print(f"📝 Transcript: {result['transcript_length']} characters")
    
    print(f"\n📄 {result['summary_type'].title()} Summary:")
    print("-"*60)
    print(result['summary'])
    
    # Ask questions
    print("\n" + "="*60)
    print("❓ ASKING QUESTIONS ABOUT THE VIDEO")
    print("="*60)
    
    questions = [
        "What is the main topic of this video?",
        "What happened with the thesis?",
        "What is the Instant Gratification Monkey?"
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. {q}")
        answer = summarizer.ask_about_video(q)
        print(f"   Answer: {answer['answer'][:200]}...")
    
    # Try AI video
    print("\n" + "="*60)
    print("📊 Summarizing 'AI Basics' video...")
    print("="*60)
    
    result2 = summarizer.summarize_video('ai_basics', 'comprehensive')
    
    print(f"\n📹 Title: {result2['title']}")
    print(f"\n📄 Summary:\n{result2['summary']}")
    
    print("\n" + "="*60)
    print("✅ Demo Complete!")
    print("="*60)
    print("\n💡 You've learned:")
    print("   ✅ How YouTube summarization works")
    print("   ✅ Different summary types")
    print("   ✅ Q&A functionality")
    print("   ✅ RAG for video content")
    print("\n🎯 Once YouTube API access is restored, the real")
    print("   summarizer will work exactly the same way!")


if __name__ == "__main__":
    demo()