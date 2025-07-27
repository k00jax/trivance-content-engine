#!/usr/bin/env python3

import os
import sys
sys.path.append('app')

from app.services.generator import generate_commentary

# Mock Article class
class MockArticle:
    def __init__(self, title, summary, link, source):
        self.title = title
        self.summary = summary
        self.link = link
        self.source = source

# Test the fix with a biopharma-style article containing HTML entities
test_article = MockArticle(
    title="Pharma&#8217;s Next Frontier: AI&#38;ML in Drug Discovery",
    summary="Recent advances in artificial intelligence and machine learning are transforming pharmaceutical research&#8230; Companies like Pfizer&#44; Novartis&#44; and Roche are investing billions in AI-driven platforms that can predict molecular behavior&#44; optimize compound selection&#44; and reduce clinical trial timelines from decades to years.",
    link="https://example.com/biopharma-ai",
    source="BioPharma Intelligence"
)

print("=== Testing OpenAI with HTML Entity Article ===")
print(f"Original title: {test_article.title}")
print(f"Original summary: {test_article.summary[:100]}...")
print("\nGenerating content...")

try:
    result = generate_commentary(test_article, "trivance_default", "LinkedIn")
    print(f"\nResult type: {type(result)}")
    print(f"Result keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
    
    if isinstance(result, dict):
        print(f"\nContent preview: {result.get('content', 'No content')[:200]}...")
        print(f"Method used: {'OpenAI' if result.get('method') == 'openai' else 'Template'}")
        if result.get('error'):
            print(f"Error: {result['error']}")
    else:
        print(f"Unexpected result format: {result}")
        
except Exception as e:
    print(f"Error during generation: {e}")
    import traceback
    traceback.print_exc()
