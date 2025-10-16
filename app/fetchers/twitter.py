import subprocess, json

def fetch_twitter_comments(keyword, limit=100):
    # Uses snscrape (no API key required) to fetch tweets matching the keyword.
    # The output parsing is simplistic: snscrape prints tweets line by line.
    try:
        cmd = ["snscrape", "--max-results", str(limit), "twitter-search", keyword]
        result = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
        tweets = []
        for line in result.splitlines():
            line = line.strip()
            if line:
                tweets.append({"text": line})
        return tweets
    except Exception as e:
        print("snscrape error:", e)
        return []
