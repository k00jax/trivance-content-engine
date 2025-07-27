#!/usr/bin/env python3
"""
Simple test for RSS content extraction enhancement
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from services.rss import clean_html, CONTENT_ENHANCEMENT_CONFIG
    import feedparser
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

def test_html_cleaning():
    """Test the HTML cleaning functionality."""
    print("🧹 Testing HTML Cleaning")
    print("=" * 30)
    
    test_cases = [
        {
            "input": "<p>This is a <strong>test</strong> with <em>HTML</em> tags.</p>",
            "expected_contains": "This is a test with HTML tags."
        },
        {
            "input": "&lt;script&gt;alert('test')&lt;/script&gt; Normal text &amp; symbols",
            "expected_contains": "Normal text & symbols"
        },
        {
            "input": "Multiple    spaces\n\nand\t\ttabs should be cleaned",
            "expected_contains": "Multiple spaces and tabs should be cleaned"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"Test {i}:")
        print(f"  Input: {case['input'][:50]}...")
        result = clean_html(case['input'])
        print(f"  Output: {result}")
        if case['expected_contains'] in result:
            print(f"  ✅ PASS")
        else:
            print(f"  ❌ FAIL - Expected to contain: {case['expected_contains']}")
        print()

def test_basic_rss_parsing():
    """Test basic RSS parsing without web scraping."""
    print("📡 Testing Basic RSS Parsing")
    print("=" * 30)
    
    # Use a simple, reliable RSS feed
    test_url = "https://feeds.npr.org/1001/rss.xml"
    
    try:
        print(f"Fetching: {test_url}")
        feed = feedparser.parse(test_url)
        
        if feed.bozo:
            print(f"⚠️  Feed parsing warning: {feed.bozo_exception}")
        
        if hasattr(feed, 'entries') and len(feed.entries) > 0:
            print(f"✅ Found {len(feed.entries)} entries")
            
            # Test first entry
            entry = feed.entries[0]
            print(f"📝 First entry: {entry.title[:60]}...")
            
            # Check available fields
            available_fields = []
            for field in ['summary', 'description', 'content']:
                if hasattr(entry, field) and getattr(entry, field):
                    content = getattr(entry, field)
                    if isinstance(content, list):
                        content_len = len(str(content[0])) if content else 0
                    else:
                        content_len = len(str(content))
                    available_fields.append(f"{field}({content_len} chars)")
            
            print(f"   Available content fields: {', '.join(available_fields)}")
            
            # Test cleaning on summary
            if hasattr(entry, 'summary'):
                raw_summary = entry.summary
                cleaned_summary = clean_html(raw_summary)
                print(f"   Raw summary length: {len(raw_summary)}")
                print(f"   Cleaned summary length: {len(cleaned_summary)}")
                print(f"   Preview: {cleaned_summary[:150]}...")
                
        else:
            print("❌ No entries found in feed")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_configuration():
    """Test the configuration settings."""
    print("⚙️  Testing Configuration")
    print("=" * 25)
    
    print(f"Enhancement enabled: {CONTENT_ENHANCEMENT_CONFIG['enabled']}")
    print(f"Max summary length: {CONTENT_ENHANCEMENT_CONFIG['max_summary_length']}")
    print(f"Extraction timeout: {CONTENT_ENHANCEMENT_CONFIG['extraction_timeout']}s")
    print(f"Min enhancement ratio: {CONTENT_ENHANCEMENT_CONFIG['min_enhancement_ratio']}")
    print(f"Min enhanced length: {CONTENT_ENHANCEMENT_CONFIG['min_enhanced_length']}")
    
    # Test configuration access
    if all(key in CONTENT_ENHANCEMENT_CONFIG for key in 
           ['enabled', 'max_summary_length', 'extraction_timeout', 
            'min_enhancement_ratio', 'min_enhanced_length']):
        print("✅ All configuration keys present")
    else:
        print("❌ Missing configuration keys")

if __name__ == "__main__":
    test_configuration()
    print()
    test_html_cleaning()
    print()
    test_basic_rss_parsing()
