"""
Test script for RSS article fetching and scoring functionality.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.rss import (
    fetch_articles_from_feed, 
    score_article, 
    get_top_article_from_all_feeds,
    get_articles_by_feed_name,
    feeds_db
)

def test_scoring():
    """Test the article scoring algorithm."""
    print("🎯 Testing Article Scoring Algorithm...")
    
    test_articles = [
        {
            "title": "ChatGPT Revolutionizes Small Business Automation",
            "summary": "Small businesses are using ChatGPT to automate customer service, streamline workflows, and improve productivity. This comprehensive guide shows practical applications for entrepreneurs."
        },
        {
            "title": "Advanced Quantum Computing Research",
            "summary": "Peer-reviewed academic study on quantum computing applications in theoretical physics. University researchers explore quantum entanglement in laboratory settings."
        },
        {
            "title": "AI Strategy for Startup Growth",
            "summary": "How AI tools help startups scale operations efficiently. Cover automation, productivity gains, and business strategy implementation."
        }
    ]
    
    for i, article in enumerate(test_articles, 1):
        score = score_article(article["title"], article["summary"])
        print(f"\nArticle {i}: {article['title']}")
        print(f"Score: {score}")
        print(f"Summary: {article['summary'][:100]}...")
        print("-" * 60)

def test_feed_parsing():
    """Test RSS feed parsing with real feeds."""
    print("\n📡 Testing RSS Feed Parsing...")
    
    # Test with TechCrunch AI feed (should be in sample data)
    test_feeds = [
        {
            "name": "TechCrunch AI",
            "url": "https://techcrunch.com/tag/artificial-intelligence/feed/"
        }
    ]
    
    for feed in test_feeds:
        print(f"\nTesting feed: {feed['name']}")
        print(f"URL: {feed['url']}")
        
        try:
            articles = fetch_articles_from_feed(feed["url"], limit=3)
            
            if articles:
                print(f"✅ Found {len(articles)} articles")
                for i, article in enumerate(articles, 1):
                    print(f"\n  Article {i}:")
                    print(f"    Title: {article['title'][:60]}...")
                    print(f"    Score: {article['score']}")
                    print(f"    Published: {article.get('published', 'Unknown')}")
                    print(f"    Summary: {article['summary'][:100]}...")
            else:
                print("❌ No articles found")
                
        except Exception as e:
            print(f"❌ Error parsing feed: {e}")
        
        print("-" * 60)

def test_top_article_selection():
    """Test automatic top article selection."""
    print("\n🏆 Testing Top Article Selection...")
    
    try:
        top_article = get_top_article_from_all_feeds()
        
        if top_article:
            print("✅ Top article found:")
            print(f"  Title: {top_article['title']}")
            print(f"  Score: {top_article['score']}")
            print(f"  Source: {top_article.get('source_feed', 'Unknown')}")
            print(f"  Link: {top_article.get('link', 'No link')}")
            print(f"  Summary: {top_article['summary'][:150]}...")
        else:
            print("❌ No top article found (no feeds or no articles)")
            
    except Exception as e:
        print(f"❌ Error getting top article: {e}")

def test_feed_specific_articles():
    """Test getting articles from specific feeds."""
    print("\n📰 Testing Feed-Specific Article Retrieval...")
    
    if not feeds_db:
        print("❌ No feeds in database. Run init_sample_data.py first.")
        return
    
    for feed in feeds_db[:2]:  # Test first 2 feeds
        print(f"\nTesting feed: {feed['name']}")
        
        try:
            articles = get_articles_by_feed_name(feed['name'], limit=2)
            
            if articles:
                print(f"✅ Found {len(articles)} articles")
                for article in articles:
                    print(f"  - {article['title'][:50]}... (Score: {article['score']})")
            else:
                print("❌ No articles found")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 RSS Functionality Test Suite")
    print("=" * 60)
    
    test_scoring()
    test_feed_parsing()
    test_top_article_selection()
    test_feed_specific_articles()
    
    print("\n✅ Testing complete!")
    print("\nNext steps:")
    print("1. Start the FastAPI server: uvicorn app.main:app --reload")
    print("2. Test the new endpoints:")
    print("   - GET /feeds/articles?feed_name=TechCrunch AI")
    print("   - GET /feeds/top-article")
    print("   - GET /feeds/articles/all")
    print("3. Launch Streamlit: streamlit run ui/streamlit_app.py")
