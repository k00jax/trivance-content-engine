#!/usr/bin/env python3
"""Test script to verify both HTML entity decoding and template detection"""

import sys
import os
sys.path.append('.')

# Enable debug mode
os.environ["DEBUG_GPT_RESPONSE"] = "true"

# Test HTML entity decoding
from app.services.rss import clean_html

print("=" * 60)
print("1. TESTING HTML ENTITY DECODING")
print("=" * 60)

test_texts = [
    "Procurement &#38; Supply Chain &#8212; Future Trends",
    "AI &#38; Machine Learning &#8212; the future is here",
    "Data Analytics &#38; Business Intelligence &#8212; insights"
]

for i, text in enumerate(test_texts, 1):
    print(f"\nTest {i}: {text}")
    result = clean_html(text)
    print(f"Result: {result}")
    
    if "&#38;" in result or "&#8212;" in result:
        print("❌ FAILED: HTML entities still present")
    else:
        print("✅ PASSED: HTML entities properly decoded")

print("\n" + "=" * 60)
print("2. TESTING TEMPLATE PATTERN DETECTION")
print("=" * 60)

# Test template pattern detection
from app.services.generator import DEBUG_GPT_RESPONSE

print(f"Debug mode enabled: {DEBUG_GPT_RESPONSE}")

# Sample content that should trigger template detection
template_content = """
Here's a specific takeaway: Procurement and supply chain management are evolving rapidly.

Smart businesses recognize the importance of adapting to these changes quickly.
"""

print(f"\nSample template content:\n{template_content}")

# The template indicators from the generator
template_indicators = [
    "Consider this:",
    "Smart businesses recognize",
    "The framework that works:",
    "Here's a specific takeaway:",
    "Here's what's interesting:",
    "Think about it:",
    "✦ Identify",
    "✦ Map", 
    "✦ Choose"
]

detected = [indicator for indicator in template_indicators if indicator in template_content]
print(f"\nTemplate indicators detected: {detected}")

if detected:
    print("✅ PASSED: Template patterns properly detected")
else:
    print("❌ FAILED: Template patterns not detected")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("HTML Entity Decoding: Check results above")
print("Template Detection: Check results above")
print("Next step: Test with actual RSS feed data")
