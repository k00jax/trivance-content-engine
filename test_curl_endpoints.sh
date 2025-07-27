#!/bin/bash

# Test script for posts.py endpoints using cURL
# Run this after starting the FastAPI server with: python -m uvicorn app.main:app --reload

echo "🧩 Testing posts.py endpoints with cURL"
echo "========================================"

# Test 1: Debug endpoint
echo "1. Testing debug endpoint..."
curl -X POST http://localhost:8000/posts/debug \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Article",
    "summary": "This is a test summary for debugging purposes",
    "source": "Test Source",
    "url": "https://example.com",
    "style": "consultative"
  }' \
  -w "\nStatus: %{http_code}\n\n"

# Test 2: Generate endpoint (correct format)
echo "2. Testing generate endpoint (correct format)..."
curl -X POST http://localhost:8000/posts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI Revolution in Small Business",
    "summary": "This comprehensive article explores how artificial intelligence is transforming small business operations, offering new opportunities for automation, customer service, and strategic decision-making.",
    "source": "MIT Technology Review",
    "link": "https://example.com/article",
    "post_style": "consultative",
    "platform": "LinkedIn"
  }' \
  -w "\nStatus: %{http_code}\n\n"

# Test 3: Generate endpoint (legacy format)
echo "3. Testing generate endpoint (legacy format)..."
curl -X POST http://localhost:8000/posts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Legacy Format Test",
    "summary": "Testing backward compatibility with the old payload format that used url and style field names.",
    "url": "https://example.com/legacy-test",
    "style": "punchy",
    "platform": "LinkedIn"
  }' \
  -w "\nStatus: %{http_code}\n\n"

# Test 4: Hashtag endpoint
echo "4. Testing hashtag endpoint..."
curl -X POST http://localhost:8000/posts/hashtags \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Artificial intelligence is revolutionizing small business operations through automation and strategic insights for entrepreneurs."
  }' \
  -w "\nStatus: %{http_code}\n\n"

echo "✅ All tests completed!"
echo "Expected results:"
echo "- Debug endpoint: 200 with received keys and payload"
echo "- Generate endpoints: 200 with post content"
echo "- Hashtag endpoint: 200 with hashtag array"
echo "- If you see 422 errors, check field names and validation"
