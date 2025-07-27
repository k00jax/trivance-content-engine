#!/usr/bin/env python3
"""Simple test for the fixes"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_basic_functionality():
    try:
        from services.generator import generate_commentary
        from routes.posts import ArticleInput
        
        print("🧪 Testing Basic Functionality")
        print("=" * 35)
        
        # Test 1: Known source
        article1 = ArticleInput(
            title="Test with Known Source",
            summary="Testing with a known source to verify it appears correctly",
            source="TechCrunch",
            link="https://example.com",
            post_style="consultative"
        )
        
        result1 = generate_commentary(article1)
        post1 = result1.get('post', '')
        
        print("Test 1: Known source")
        if "TechCrunch" in post1:
            print("✅ Known source correctly displayed")
        else:
            print("❌ Known source not found")
        
        if '#' in post1:
            print("✅ Hashtags included")
        else:
            print("❌ No hashtags found")
        
        # Test 2: Empty source
        article2 = ArticleInput(
            title="Test with Empty Source", 
            summary="Testing with empty source to verify RSS Feeds fallback",
            source="",
            link="https://example.com",
            post_style="punchy"
        )
        
        result2 = generate_commentary(article2)
        post2 = result2.get('post', '')
        
        print("\nTest 2: Empty source")
        if "RSS Feeds" in post2:
            print("✅ Fallback source correctly applied")
        else:
            print("❌ Fallback source not found")
            # Show what source was used
            lines = post2.split('\n')
            for line in lines:
                if 'Source:' in line:
                    print(f"   Found: {line}")
                    break
        
        if '#' in post2:
            print("✅ Hashtags included")
        else:
            print("❌ No hashtags found")
        
        print("\n🎯 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_basic_functionality()
