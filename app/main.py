from fastapi import FastAPI, HTTPException
from .fetchers.youtube import fetch_youtube_comments
from .fetchers.reddit import fetch_reddit_comments
from .fetchers.twitter import fetch_twitter_comments
from .analyzer import cluster_and_summarize
from .db import cache_get, cache_set

app = FastAPI(title="CommentScope API")

@app.get("/")
def read_root():
    return {"message": "Public Data Aggregator API is running!"}

@app.get("/api/painpoints")
def get_painpoints(source: str, id_or_keyword: str, clusters: int = 5):
    cache_key = f"{source}:{id_or_keyword}:{clusters}"
    cached = cache_get(cache_key)
    if cached:
        return cached

    if source == "youtube":
        comments = fetch_youtube_comments(id_or_keyword)
    elif source == "reddit":
        comments = fetch_reddit_comments(id_or_keyword)
    elif source == "twitter":
        comments = fetch_twitter_comments(id_or_keyword)
    else:
        raise HTTPException(status_code=400, detail="unsupported source")

    summaries = cluster_and_summarize(comments, n_clusters=clusters)
    result = {"source": source, "query": id_or_keyword, "painpoints": summaries}
    cache_set(cache_key, result)
    return result
