#!/usr/bin/env python3
"""Test RSS feed source assignment"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_feed_source_assignment():
    try:
        from services.rss import feeds_db, get_feed_name_by_url, fetch_articles_from_feed
        
        print("🔧 Testing Feed Source Assignment")
        print("=" * 40)
        
        print(f"Found {len(feeds_db)} feeds in database:")
        for feed in feeds_db:
            print(f"  - {feed['name']}: {feed['url']}")
        
        if feeds_db:
            # Test the helper function
            print(f"\n🧪 Testing get_feed_name_by_url helper:")
            test_feed = feeds_db[0]
            result = get_feed_name_by_url(test_feed['url'])
            print(f"URL: {test_feed['url']}")
            print(f"Expected name: {test_feed['name']}")
            print(f"Helper result: {result}")
            
            if result == test_feed['name']:
                print("✅ Helper function works correctly")
            else:
                print("❌ Helper function mismatch")
            
            # Test with unknown URL
            unknown_result = get_feed_name_by_url("https://unknown-feed.com/rss")
            print(f"\nUnknown URL test: {unknown_result} (should be None)")
            
            if unknown_result is None:
                print("✅ Unknown URL correctly returns None")
            else:
                print("❌ Unknown URL should return None")
            
            print(f"\n📰 Testing article fetching with source assignment:")
            print("(Note: This will attempt to fetch real articles, may take a moment)")
            
            # Test fetching articles from first feed
            try:
                articles = fetch_articles_from_feed(test_feed['url'], limit=2)
                
                if articles:
                    print(f"✅ Fetched {len(articles)} articles from {test_feed['name']}")
                    
                    for i, article in enumerate(articles):
                        print(f"\nArticle {i+1}:")
                        print(f"  Title: {article.get('title', 'No title')[:50]}...")
                        print(f"  Source: {article.get('source', 'No source')}")
                        print(f"  Score: {article.get('score', 0)}")
                        
                        # Verify source is correct
                        if article.get('source') == test_feed['name']:
                            print("  ✅ Source correctly assigned")
                        else:
                            print(f"  ❌ Source mismatch. Expected: {test_feed['name']}, Got: {article.get('source')}")
                else:
                    print("⚠️ No articles fetched (feed may be down or empty)")
                    
            except Exception as e:
                print(f"⚠️ Error fetching articles: {e}")
        else:
            print("No feeds found in database")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_feed_source_assignment()
