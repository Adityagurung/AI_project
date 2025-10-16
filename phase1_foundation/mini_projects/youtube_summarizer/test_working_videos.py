"""
Test multiple known-working videos to find ones that work for you
"""
from youtube_transcript_api import YouTubeTranscriptApi

# List of videos that typically have transcripts
test_videos = [
    ("Rick Astley - Never Gonna Give You Up", "dQw4w9WgXcQ"),
    ("Python Tutorial", "rfscVS0vtbw"),
    ("Minecraft Video", "9bZkp7q19f0"),
    ("Educational Content", "kJQP7kiw5Fk"),
    ("Tech Talk", "cKxRvEZd3Mw"),
]

print("Testing multiple videos to find working ones...\n")
print("="*60)

working_videos = []
failed_videos = []

for name, video_id in test_videos:
    print(f"\nTesting: {name}")
    print(f"Video ID: {video_id}")
    
    try:
        # First, try to list available transcripts
        print("  Checking transcripts...")
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Get list of available languages
        available = []
        for transcript in transcript_list:
            available.append(f"{transcript.language} ({transcript.language_code})")
        
        print(f"  ✅ Available languages: {', '.join(available)}")
        
        # Try to fetch the transcript
        print("  Fetching transcript...")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        print(f"  ✅ SUCCESS! Got {len(transcript)} segments")
        print(f"  First text: '{transcript[0]['text'][:50]}...'")
        
        working_videos.append((name, video_id))
        
    except Exception as e:
        print(f"  ❌ Failed: {type(e).__name__}: {str(e)[:100]}")
        failed_videos.append((name, video_id, str(e)))

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

if working_videos:
    print(f"\n✅ {len(working_videos)} videos worked:")
    for name, video_id in working_videos:
        print(f"   - {name}")
        print(f"     https://www.youtube.com/watch?v={video_id}")
else:
    print("\n❌ No videos worked!")
    print("\nPossible issues:")
    print("  - Your network/firewall is blocking YouTube API")
    print("  - Your region has restrictions")
    print("  - YouTube is blocking automated access from your IP")

if failed_videos:
    print(f"\n❌ {len(failed_videos)} videos failed:")
    for name, video_id, error in failed_videos:
        error_type = error.split(':')[0] if ':' in error else error[:50]
        print(f"   - {name}: {error_type}")

print("\n" + "="*60)