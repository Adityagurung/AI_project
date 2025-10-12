"""
Debug YouTube Transcript API installation
"""
import sys

print("="*60)
print("YOUTUBE TRANSCRIPT API DEBUG")
print("="*60)

# Check Python environment
print(f"\nPython: {sys.version}")
print(f"Executable: {sys.executable}")

# Try to import
print("\n1. Attempting import...")
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print("   ✅ Import successful")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Check what's available
print("\n2. Class type:", type(YouTubeTranscriptApi))

print("\n3. All attributes:")
all_attrs = dir(YouTubeTranscriptApi)
for attr in all_attrs:
    if not attr.startswith('_'):
        print(f"   - {attr}")

print("\n4. Checking critical methods:")
for method in ['get_transcript', 'list_transcripts', 'get_transcripts']:
    exists = hasattr(YouTubeTranscriptApi, method)
    status = "✅" if exists else "❌"
    print(f"   {status} {method}")
    
    if exists:
        # Get method info
        method_obj = getattr(YouTubeTranscriptApi, method)
        print(f"      Type: {type(method_obj)}")

print("\n5. Trying to call get_transcript...")
try:
    # This should work even if video doesn't have transcript
    result = YouTubeTranscriptApi.get_transcript('test123')
    print(f"   ✅ Method callable (got result: {type(result)})")
except AttributeError as e:
    print(f"   ❌ AttributeError: {e}")
except Exception as e:
    print(f"   ✅ Method callable (got expected error: {type(e).__name__})")

print("\n" + "="*60)