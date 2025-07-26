"""
Quick API endpoint testing for RSS functionality.
Run this after starting the FastAPI server.
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_endpoints():
    print("🌐 Testing RSS API Endpoints")
    print("=" * 50)
    
    # Test 1: Get feeds
    print("1. Testing GET /feeds/")
    try:
        res = requests.get(f"{API_URL}/feeds/")
        print(f"   Status: {res.status_code}")
        feeds = res.json()
        print(f"   Feeds found: {len(feeds)}")
        for feed in feeds:
            print(f"   - {feed['name']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 2: Get articles from specific feed
    print("2. Testing GET /feeds/articles")
    try:
        res = requests.get(f"{API_URL}/feeds/articles", params={"feed_name": "TechCrunch AI"})
        print(f"   Status: {res.status_code}")
        if res.status_code == 200:
            articles = res.json()
            print(f"   Articles found: {len(articles)}")
            for article in articles[:2]:
                print(f"   - {article['title'][:50]}... (Score: {article['score']})")
        else:
            print(f"   Error: {res.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 3: Get top article
    print("3. Testing GET /feeds/top-article")
    try:
        res = requests.get(f"{API_URL}/feeds/top-article")
        print(f"   Status: {res.status_code}")
        if res.status_code == 200:
            article = res.json()
            print(f"   Top article: {article['title'][:50]}...")
            print(f"   Score: {article['score']}")
            print(f"   Source: {article.get('source_feed', 'Unknown')}")
        else:
            print(f"   Error: {res.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test 4: Get all articles
    print("4. Testing GET /feeds/articles/all")
    try:
        res = requests.get(f"{API_URL}/feeds/articles/all")
        print(f"   Status: {res.status_code}")
        if res.status_code == 200:
            articles = res.json()
            print(f"   Total articles: {len(articles)}")
            print("   Top 3 by score:")
            for article in articles[:3]:
                print(f"   - {article['title'][:40]}... (Score: {article['score']}) from {article['source_feed']}")
        else:
            print(f"   Error: {res.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    print("⚡ Quick API Test")
    print("Make sure FastAPI server is running: uvicorn app.main:app --reload")
    print()
    
    try:
        # Quick health check
        requests.get(f"{API_URL}/feeds/", timeout=2)
        test_endpoints()
        print("\n✅ All endpoint tests completed!")
    except requests.ConnectionError:
        print("❌ Cannot connect to API server.")
        print("Start the server first: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
