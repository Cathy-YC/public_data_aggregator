import requests

def fetch_reddit_comments(thread_url):
    if not thread_url.endswith(".json"):
        thread_url += ".json"
    resp = requests.get(thread_url, headers={"User-Agent": "CommentScope"}, timeout=15)
    data = resp.json()
    comments = []
    # Reddit returns listing: [post, comments]
    try:
        for child in data[1]["data"]["children"]:
            body = child["data"].get("body")
            if body:
                comments.append({"text": body, "author": child["data"].get("author")})
    except Exception:
        pass
    return comments
