from youtube_summarizer import YouTubeSummarizer

summarizer = YouTubeSummarizer()

# This video definitely has transcripts
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

print("Testing with Rick Astley video (definitely has transcripts)...")
print("⏳ Processing...\n")

try:
    result = summarizer.summarize_video(video_url, summary_type='brief')
    
    print("✅ SUCCESS!\n")
    print("="*60)
    print(f"📊 Duration: {result['duration']} seconds")
    print(f"📝 Transcript: {result['transcript_length']} characters")
    print("="*60)
    print(f"\n📄 Summary:\n\n{result['summary']}")
    
except Exception as e:
    print(f"❌ Error: {e}")