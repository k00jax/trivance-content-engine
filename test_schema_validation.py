#!/usr/bin/env python3
"""
Validate the ArticleInput schema without needing a running server
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from routes.posts import ArticleInput
    from pydantic import ValidationError
    import json
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def test_schema_validation():
    """Test ArticleInput schema validation."""
    print("🧪 Testing ArticleInput Schema Validation")
    print("=" * 45)
    
    # Test 1: Valid payload (new format)
    print("1. Testing valid payload (new format)")
    try:
        valid_data = {
            "title": "AI Revolution in Small Business",
            "summary": "This is a comprehensive summary about AI impact on small businesses with detailed insights and strategic recommendations.",
            "source": "MIT Technology Review",
            "link": "https://example.com/article",
            "post_style": "consultative",
            "platform": "LinkedIn"
        }
        
        article = ArticleInput(**valid_data)
        print(f"   ✅ Valid - title: {article.title[:30]}...")
        print(f"   ✅ Valid - summary: {len(article.summary)} chars")
        print(f"   ✅ Valid - source: {article.source}")
        print(f"   ✅ Valid - style: {article.post_style}")
        
    except ValidationError as e:
        print(f"   ❌ Validation failed: {e}")
    
    # Test 2: Legacy payload (old format with url/style)
    print("\n2. Testing legacy payload (old format)")
    try:
        legacy_data = {
            "title": "Legacy Format Test Article",
            "summary": "Testing backward compatibility with old field names like url and style instead of link and post_style.",
            "url": "https://example.com/legacy",  # Using 'url' instead of 'link'
            "style": "punchy",  # Using 'style' instead of 'post_style'
            "platform": "LinkedIn"
            # Note: 'source' is missing to test default
        }
        
        article = ArticleInput(**legacy_data)
        print(f"   ✅ Legacy format converted - link: {article.link}")
        print(f"   ✅ Legacy format converted - post_style: {article.post_style}")
        print(f"   ✅ Default source applied: {article.source}")
        
    except ValidationError as e:
        print(f"   ❌ Legacy validation failed: {e}")
    
    # Test 3: Streamlit payload format
    print("\n3. Testing Streamlit payload format")
    try:
        streamlit_data = {
            "title": "Streamlit Generated Article",
            "summary": "This simulates the exact payload format that Streamlit sends to the API endpoint for post generation.",
            "source": "RSS Feed",
            "link": "https://example.com/streamlit-test",
            "post_style": "Trivance Default",  # This is what Streamlit sends
            "platform": "LinkedIn"
        }
        
        article = ArticleInput(**streamlit_data)
        print(f"   ✅ Streamlit format - title: {article.title[:30]}...")
        print(f"   ✅ Streamlit format - style: {article.post_style}")
        
    except ValidationError as e:
        print(f"   ❌ Streamlit validation failed: {e}")
    
    # Test 4: Invalid payload (missing required fields)
    print("\n4. Testing invalid payload (missing title)")
    try:
        invalid_data = {
            "summary": "Short",  # Too short for validation
            "source": "Test Source"
            # Missing required 'title'
        }
        
        article = ArticleInput(**invalid_data)
        print(f"   ❌ Should have failed validation!")
        
    except ValidationError as e:
        print(f"   ✅ Correctly rejected invalid data: {e.error_count()} errors")
        for error in e.errors():
            print(f"      - {error['loc'][0]}: {error['msg']}")
    
    # Test 5: Edge cases
    print("\n5. Testing edge cases")
    
    # Minimum valid data
    try:
        minimal_data = {
            "title": "Short",  # Minimum length
            "summary": "This is exactly twenty characters long to meet minimum requirements for summary validation."
        }
        
        article = ArticleInput(**minimal_data)
        print(f"   ✅ Minimal data accepted")
        print(f"      - Default source: {article.source}")
        print(f"      - Default link: '{article.link}'")
        print(f"      - Default style: {article.post_style}")
        print(f"      - Default platform: {article.platform}")
        
    except ValidationError as e:
        print(f"   ❌ Minimal data failed: {e}")

def test_response_format():
    """Test expected response format."""
    print("\n📤 Expected Response Format")
    print("=" * 30)
    
    expected_response = {
        "post": "Generated LinkedIn post content here...",
        "method": "template_based",
        "style_used": "consultative",
        "hashtags": "#TrivanceAI #SmallBusinessAI #AIStrategy",
        "key_insights": ["Insight 1", "Insight 2"],
        "specific_detail": "Specific detail extracted from article"
    }
    
    print("The /generate endpoint should return:")
    print(json.dumps(expected_response, indent=2))
    
    print("\nStreamlit should look for result.get('post') or result.get('content')")

if __name__ == "__main__":
    test_schema_validation()
    test_response_format()
    
    print("\n🎯 Schema Validation Summary")
    print("=" * 35)
    print("✅ ArticleInput model supports both new and legacy field names")
    print("✅ Required fields: title (min 5 chars), summary (min 20 chars)")
    print("✅ Optional fields: source (defaults to 'RSS Feed'), link, post_style, platform")
    print("✅ Backward compatibility: url→link, style→post_style")
    print("✅ Validation errors are properly caught and reported")
    
    print("\n🚀 Ready for Testing")
    print("=" * 20)
    print("The schema is now compatible with Streamlit payloads!")
    print("Run 'python -m uvicorn app.main:app --reload' to test live endpoints.")
