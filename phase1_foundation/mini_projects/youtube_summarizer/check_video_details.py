"""
Check detailed information about a specific video
"""
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import requests

video_id = "5iPH-br_eJQ"
video_url = f"https://www.youtube.com/watch?v={video_id}"

print(f"Checking video: {video_id}")
print(f"URL: {video_url}")
print("="*60)

# 1. Check if video page loads
print("\n1. Testing if video page is accessible...")
try:
    response = requests.get(video_url, timeout=10)
    print(f"   ✅ Page loads (Status: {response.status_code})")
except Exception as e:
    print(f"   ❌ Cannot access page: {e}")

# 2. Try to list transcripts
print("\n2. Checking available transcripts...")
try:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
    print("   ✅ Transcripts are available!")
    print("\n   Available transcripts:")
    
    for transcript in transcript_list:
        is_generated = " (auto-generated)" if transcript.is_generated else ""
        is_translatable = " [translatable]" if transcript.is_translatable else ""
        print(f"   - {transcript.language} ({transcript.language_code}){is_generated}{is_translatable}")
    
    # 3. Try to fetch each transcript
    print("\n3. Trying to fetch transcripts...")
    for transcript in transcript_list:
        try:
            print(f"\n   Fetching: {transcript.language_code}")
            data = transcript.fetch()
            print(f"   ✅ Success! {len(data)} segments")
            print(f"   First segment: '{data[0]['text'][:50]}...'")
            break  # Successfully got one, that's enough
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
except TranscriptsDisabled:
    print("   ❌ Transcripts are disabled for this video")
except NoTranscriptFound:
    print("   ❌ No transcripts found")
except Exception as e:
    print(f"   ❌ Error: {type(e).__name__}: {e}")

# 4. Try direct get_transcript call
print("\n4. Trying direct YouTubeTranscriptApi.get_transcript()...")
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    print(f"   ✅ Success! {len(transcript)} segments")
except Exception as e:
    print(f"   ❌ Failed: {type(e).__name__}: {e}")
    
    # Try with different languages
    print("\n5. Trying with explicit language codes...")
    for lang in ['en', 'hi', 'en-US', 'en-GB']:
        try:
            print(f"   Trying language: {lang}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
            print(f"   ✅ Success with {lang}! {len(transcript)} segments")
            break
        except Exception as e2:
            print(f"   ❌ {lang} failed: {str(e2)[:50]}")

print("\n" + "="*60)