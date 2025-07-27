#!/usr/bin/env python3
"""
Test script for the enhanced posts.py endpoints
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_debug_endpoint():
    """Test the debug endpoint to see what we're sending."""
    print("🧪 Testing Debug Endpoint")
    print("=" * 30)
    
    test_payload = {
        "title": "Test Article About AI",
        "summary": "This is a comprehensive summary about artificial intelligence and its impact on small businesses. It covers various aspects of AI implementation and strategy.",
        "source": "MIT Technology Review",
        "link": "https://example.com/article",
        "post_style": "consultative", 
        "platform": "LinkedIn"
    }
    
    try:
        response = requests.post(f"{API_URL}/posts/debug", json=test_payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Debug endpoint working!")
            print(f"Received keys: {result['received_keys']}")
            print(f"Payload types: {result['payload_types']}")
        else:
            print(f"❌ Debug endpoint failed: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ Connection error: {e}")

def test_generate_endpoint():
    """Test the generate endpoint with proper schema."""
    print("\n🚀 Testing Generate Endpoint")
    print("=" * 30)
    
    test_payload = {
        "title": "AI Revolution in Small Business",
        "summary": "Artificial intelligence is transforming how small businesses operate, offering new opportunities for automation, customer service, and strategic decision-making. This comprehensive guide explores practical AI applications for SMBs.",
        "source": "MIT Technology Review",
        "link": "https://example.com/ai-small-business",
        "post_style": "consultative",
        "platform": "LinkedIn"
    }
    
    try:
        response = requests.post(f"{API_URL}/posts/generate", json=test_payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Generate endpoint working!")
            print(f"Response keys: {list(result.keys())}")
            
            if "post" in result:
                print(f"Generated post preview: {result['post'][:100]}...")
            else:
                print("⚠️ No 'post' field in response")
                print(f"Full response: {json.dumps(result, indent=2)}")
                
        else:
            print(f"❌ Generate endpoint failed: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ Connection error: {e}")

def test_alternative_payload():
    """Test with the old payload format (using url/style instead of link/post_style)."""
    print("\n🔄 Testing Backward Compatibility")
    print("=" * 30)
    
    # Old format that Streamlit was sending
    test_payload = {
        "title": "Legacy Format Test",
        "summary": "Testing backward compatibility with the old payload format that used 'url' and 'style' field names.",
        "url": "https://example.com/legacy-test",  # Using 'url' instead of 'link'
        "style": "punchy",  # Using 'style' instead of 'post_style'
        "platform": "LinkedIn"
        # Note: 'source' is missing to test default handling
    }
    
    try:
        response = requests.post(f"{API_URL}/posts/generate", json=test_payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Backward compatibility working!")
            
            if "post" in result:
                print(f"Generated post preview: {result['post'][:100]}...")
            else:
                print("⚠️ No 'post' field in response")
                print(f"Full response: {json.dumps(result, indent=2)}")
                
        elif response.status_code == 422:
            print("❌ 422 Validation Error - schema mismatch:")
            error_details = response.json()
            print(json.dumps(error_details, indent=2))
            
        else:
            print(f"❌ Generate endpoint failed: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ Connection error: {e}")

def test_hashtag_endpoint():
    """Test hashtag generation endpoint."""
    print("\n🏷️ Testing Hashtag Endpoint")
    print("=" * 30)
    
    test_payload = {
        "content": "Artificial intelligence is revolutionizing small business operations through automation and strategic insights for entrepreneurs."
    }
    
    try:
        response = requests.post(f"{API_URL}/posts/hashtags", json=test_payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Hashtag endpoint working!")
            print(f"Generated hashtags: {result.get('hashtags', [])}")
        else:
            print(f"❌ Hashtag endpoint failed: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print("🧩 Posts.py Endpoint Testing")
    print("=" * 40)
    print("Make sure the FastAPI server is running:")
    print("python -m uvicorn app.main:app --reload")
    print()
    
    test_debug_endpoint()
    test_generate_endpoint() 
    test_alternative_payload()
    test_hashtag_endpoint()
    
    print("\n🎯 Test Summary")
    print("=" * 20)
    print("If all tests pass, the posts.py endpoints are working correctly!")
    print("If you see 422 errors, check the payload field names and types.")
    print("If you see connection errors, make sure the FastAPI server is running.")
