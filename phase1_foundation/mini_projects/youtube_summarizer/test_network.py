"""
Test network connectivity to YouTube
"""
import requests

print("Testing network connectivity...\n")

urls = [
    ("YouTube Home", "https://www.youtube.com"),
    ("YouTube API", "https://www.youtube.com/api/timedtext"),
    ("Test Video", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
]

for name, url in urls:
    try:
        response = requests.get(url, timeout=10)
        status = "✅" if response.status_code == 200 else f"⚠️  ({response.status_code})"
        print(f"{status} {name}")
    except Exception as e:
        print(f"❌ {name}: {e}")