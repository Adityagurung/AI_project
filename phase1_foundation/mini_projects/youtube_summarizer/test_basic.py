"""
Basic test to verify youtube-transcript-api is working
"""
from youtube_transcript_api import YouTubeTranscriptApi

print("Testing YouTube Transcript API...\n")

# First, verify the methods exist
print("1. Checking if required methods exist:")
methods_to_check = ['get_transcript', 'list_transcripts']
for method_name in methods_to_check:
    exists = hasattr(YouTubeTranscriptApi, method_name)
    print(f"   {'✅' if exists else '❌'} {method_name}")

if not hasattr(YouTubeTranscriptApi, 'get_transcript'):
    print("\n❌ Package is still broken. Try installing from GitHub:")
    print("   pip uninstall youtube-transcript-api -y")
    print("   pip install git+https://github.com/jdepoix/youtube-transcript-api.git")
    exit(1)

# Now test with an actual video
print("\n2. Testing with a real video:")
test_video_id = "5iPH-br_eJQ"  # Your video

try:
    print(f"   Fetching transcript for video: {test_video_id}")
    transcript = YouTubeTranscriptApi.get_transcript(test_video_id)
    
    print(f"   ✅ Success! Retrieved {len(transcript)} transcript segments")
    print(f"   First segment: {transcript[0]['text'][:50]}...")
    print(f"   Video duration: approximately {transcript[-1]['start']:.0f} seconds")
    
    print("\n✅ Everything is working correctly!")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("\n   This could mean:")
    print("   - The video doesn't have captions enabled")
    print("   - The video is region-restricted")
    print("   - YouTube changed their API")