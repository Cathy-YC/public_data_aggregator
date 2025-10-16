from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from langdetect import detect
from googletrans import Translator
import os
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

translator = Translator()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def detect_and_translate(texts):
    translated = []
    for t in texts:
        try:
            lang = detect(t)
            if lang != "en":
                t = translator.translate(t, src=lang, dest="en").text
        except Exception:
            # if detection/translation fails, keep original
            pass
        translated.append(t)
    return translated

def _summarize_with_openai(text_snippet):
    if OpenAI is None or not OPENAI_KEY:
        # fallback: simple heuristic summary
        lines = text_snippet.splitlines()
        return lines[0] if lines else ""
    client = OpenAI(api_key=OPENAI_KEY)
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content": "Summarize the main painpoints users mention:\n" + text_snippet}]
        )
        return resp.choices[0].message.content
    except Exception as e:
        print("OpenAI error:", e)
        return (text_snippet.splitlines()[0] if text_snippet else "")

def cluster_and_summarize(comments, n_clusters=5):
    texts = [c.get("text","") for c in comments if c.get("text")]
    if not texts:
        return []

    texts_en = detect_and_translate(texts)

    max_clusters = min(n_clusters, len(texts_en))
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    X = vectorizer.fit_transform(texts_en)
    kmeans = KMeans(n_clusters=max_clusters, random_state=42).fit(X)

    clusters = [[] for _ in range(max_clusters)]
    for i, label in enumerate(kmeans.labels_):
        clusters[label].append(texts_en[i])

    summaries = []
    for group in clusters:
        if not group:
            continue
        joined = "\n".join(group[:10])
        summary = _summarize_with_openai(joined)
        summaries.append(summary)
    return summaries
