from youtube_summarizer import YouTubeSummarizer

summarizer = YouTubeSummarizer()

# This TED Talk definitely has transcripts
video_url = "https://www.youtube.com/watch?v=c0KYU2j0TM4"

print("📹 Testing with TED Talk: 'Inside the mind of a master procrastinator'")
print("⏳ Processing (this may take 30-60 seconds)...\n")

try:
    result = summarizer.summarize_video(video_url, 'brief')
    
    print("✅ Success!\n")
    print("="*60)
    print(f"📊 Duration: {result['duration']} seconds")
    print(f"📝 Transcript: {result['transcript_length']} characters")
    print("="*60)
    print(f"\n📄 Summary:\n\n{result['summary']}")
    print("\n" + "="*60)
    
    # Try asking a question
    print("\n❓ Asking: 'What is the main topic?'")
    answer = summarizer.ask_about_video("What is the main topic?")
    print(f"\n🤖 Answer:\n{answer['answer']}")
    
except Exception as e:
    print(f"❌ Error: {e}")