import redis
import json
from .config import REDIS_URL

r = redis.from_url(REDIS_URL)

def cache_set(key, value, expire=3600):
    try:
        r.set(key, json.dumps(value), ex=expire)
    except Exception as e:
        # fallback: ignore cache errors
        print("Redis set error:", e)

def cache_get(key):
    try:
        val = r.get(key)
        return json.loads(val) if val else None
    except Exception as e:
        print("Redis get error:", e)
        return None
