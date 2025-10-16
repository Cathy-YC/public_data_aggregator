import requests
from ..config import YOUTUBE_API_KEY

def fetch_youtube_comments(video_id, max_results=100):
    # Note: YouTube API paginates; this is a simplified single-page fetch.
    url = f"https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": YOUTUBE_API_KEY,
        "maxResults": min(max_results, 100)
    }
    resp = requests.get(url, params=params, timeout=15)
    data = resp.json()
    comments = []
    for item in data.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "text": snippet.get("textDisplay",""),
            "author": snippet.get("authorDisplayName"),
            "likes": snippet.get("likeCount", 0)
        })
    return comments
