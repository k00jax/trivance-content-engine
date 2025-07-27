#!/usr/bin/env python3
"""Test script to verify HTML entity decoding fix"""

import sys
import os
sys.path.append('.')

from app.services.rss import clean_html

# Test cases from the posts.json
test_cases = [
    "Procurement &#38; Supply Chain &#8212; Future Trends",
    "AI &#38; Machine Learning &#8212; the future is here",
    "Data Analytics &#38; Business Intelligence &#8212; insights that matter"
]

print("Testing HTML Entity Decoding Fix")
print("=" * 50)

for i, test_text in enumerate(test_cases, 1):
    print(f"\nTest {i}:")
    print(f"Before: {repr(test_text)}")
    
    result = clean_html(test_text)
    print(f"After:  {repr(result)}")
    
    # Check if entities were properly decoded
    if "&#38;" in result or "&#8212;" in result:
        print("❌ FAILED: HTML entities still present")
    else:
        print("✅ PASSED: HTML entities properly decoded")

print("\n" + "=" * 50)
print("HTML Entity Decoding Test Complete")
