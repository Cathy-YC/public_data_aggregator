import requests
import pytest

BASE_URL = "http://localhost:8011"  # Docker容器映射的端口

def test_root():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200

# def test_search():
#     payload = {"query": "AI创业机会"}
#     r = requests.post(f"{BASE_URL}/api/search", json=payload)
#     assert r.status_code == 200
#     data = r.json()
#     assert "results" in data

# def test_summary():
#     payload = {"text": "人工智能创业正在快速发展"}
#     r = requests.post(f"{BASE_URL}/api/summary", json=payload)
#     assert r.status_code == 200
#     data = r.json()
#     assert "summary" in data