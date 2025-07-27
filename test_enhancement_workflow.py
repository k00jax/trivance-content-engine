#!/usr/bin/env python3
"""
Test the full RSS enhancement workflow
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from services.rss import enhance_rss_summary, CONTENT_ENHANCEMENT_CONFIG
    import feedparser
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def test_enhancement_workflow():
    """Test the complete enhancement workflow."""
    print("🚀 Testing Complete RSS Enhancement Workflow")
    print("=" * 50)
    
    # Use NPR feed as it's reliable
    test_url = "https://feeds.npr.org/1001/rss.xml"
    
    try:
        print(f"Fetching feed: {test_url}")
        feed = feedparser.parse(test_url)
        
        if not feed.entries:
            print("❌ No entries found")
            return
            
        print(f"✅ Found {len(feed.entries)} entries")
        
        # Test enhancement on first few entries
        for i, entry in enumerate(feed.entries[:3], 1):
            print(f"\n📄 Entry {i}: {entry.title[:60]}...")
            
            # Get original summary info
            original_summary = getattr(entry, 'summary', '')
            print(f"   Original summary length: {len(original_summary)}")
            
            # Test enhancement
            enhanced_summary = enhance_rss_summary(entry)
            print(f"   Enhanced summary length: {len(enhanced_summary)}")
            
            # Determine if enhancement occurred
            enhancement_ratio = len(enhanced_summary) / len(original_summary) if original_summary else 0
            
            if enhancement_ratio >= CONTENT_ENHANCEMENT_CONFIG['min_enhancement_ratio']:
                print(f"   ✅ ENHANCED (ratio: {enhancement_ratio:.1f}x)")
            elif len(enhanced_summary) >= CONTENT_ENHANCEMENT_CONFIG['min_enhanced_length']:
                print(f"   ✅ SUFFICIENT LENGTH ({len(enhanced_summary)} chars)")
            else:
                print(f"   ⚠️  MAY NEED ENHANCEMENT ({len(enhanced_summary)} chars)")
            
            # Show preview
            preview = enhanced_summary[:150]
            if len(enhanced_summary) > 150:
                preview += "..."
            print(f"   Preview: {preview}")
            
            # Check quality indicators
            quality_indicators = []
            if '.' in enhanced_summary:
                sentence_count = enhanced_summary.count('.')
                quality_indicators.append(f"{sentence_count} sentences")
            
            if any(word in enhanced_summary.lower() for word in ['said', 'according', 'reported']):
                quality_indicators.append("attribution found")
                
            if len(enhanced_summary.split()) > 20:
                quality_indicators.append("substantial content")
                
            print(f"   Quality: {', '.join(quality_indicators) if quality_indicators else 'basic content'}")
        
        print(f"\n📊 Enhancement Summary:")
        print(f"   Configuration: {CONTENT_ENHANCEMENT_CONFIG['enabled']} enabled")
        print(f"   Min length target: {CONTENT_ENHANCEMENT_CONFIG['min_enhanced_length']} chars")
        print(f"   Enhancement ratio: {CONTENT_ENHANCEMENT_CONFIG['min_enhancement_ratio']}x")
        print(f"   Max length: {CONTENT_ENHANCEMENT_CONFIG['max_summary_length']} chars")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhancement_workflow()
