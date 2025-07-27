#!/usr/bin/env python3
"""
Test script for enhanced RSS content extraction
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from services.rss import fetch_articles_from_feed, enhance_rss_summary, CONTENT_ENHANCEMENT_CONFIG
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

def test_rss_feeds():
    """Test enhanced RSS extraction with real feeds."""
    
    print("🔧 Testing Enhanced RSS Content Extraction")
    print("=" * 50)
    
    # Test feeds - using popular news sources
    test_feeds = [
        {
            "url": "https://feeds.bbci.co.uk/news/rss.xml",
            "name": "BBC News"
        },
        {
            "url": "https://rss.cnn.com/rss/edition.rss", 
            "name": "CNN"
        },
        {
            "url": "https://feeds.npr.org/1001/rss.xml",
            "name": "NPR News"
        }
    ]
    
    print(f"Configuration:")
    print(f"  Enhancement enabled: {CONTENT_ENHANCEMENT_CONFIG['enabled']}")
    print(f"  Max summary length: {CONTENT_ENHANCEMENT_CONFIG['max_summary_length']}")
    print(f"  Extraction timeout: {CONTENT_ENHANCEMENT_CONFIG['extraction_timeout']}s")
    print(f"  Min enhancement ratio: {CONTENT_ENHANCEMENT_CONFIG['min_enhancement_ratio']}")
    print(f"  Min enhanced length: {CONTENT_ENHANCEMENT_CONFIG['min_enhanced_length']}")
    print()
    
    for feed in test_feeds:
        print(f"📰 Testing {feed['name']}")
        print(f"   URL: {feed['url']}")
        
        try:
            # Fetch articles from the feed
            articles = fetch_articles_from_feed(feed['url'])
            
            if articles:
                print(f"   ✅ Found {len(articles)} articles")
                
                # Test the first article
                first_article = articles[0]
                print(f"   📝 First Article: {first_article.get('title', 'No title')[:60]}...")
                
                original_length = len(first_article.get('summary', ''))
                print(f"      Original summary length: {original_length} characters")
                
                if original_length > 0:
                    # Show first 150 chars of summary
                    summary_preview = first_article['summary'][:150]
                    if len(first_article['summary']) > 150:
                        summary_preview += "..."
                    print(f"      Summary preview: {summary_preview}")
                    
                    # Check if it looks enhanced
                    if original_length >= CONTENT_ENHANCEMENT_CONFIG['min_enhanced_length']:
                        print(f"      ✅ Summary appears to be enhanced (length: {original_length})")
                    else:
                        print(f"      ⚠️  Summary may be truncated (length: {original_length})")
                else:
                    print(f"      ❌ No summary content found")
                    
            else:
                print(f"   ❌ No articles found")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print()

if __name__ == "__main__":
    test_rss_feeds()
