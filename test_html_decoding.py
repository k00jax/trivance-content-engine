"""
Test HTML entity decoding in template generation
"""
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.generator import generate_template_based

class MockArticleWithEntities:
    def __init__(self):
        self.title = "Zifo Survey: AI Gains in Biopharma, Data Readiness Challenges"
        self.summary = "A new survey of scientists and informaticians reveals that while investment in artificial intelligence (AI) and machine learning (ML) is rapidly accelerating across the R&#38;D, manufacturing, and clinical value chain, persistent data silos and integration headaches are stalling progress &#8212; raising crucial questions about whether science-focused companies are truly ready"
        self.source = "AI-TechPark"
        self.link = "https://ai-techpark.com/zifo-survey-ai-gains-in-biopharma-data-readiness-challenges/"

print("🧪 HTML Entity Decoding Test")
print("=" * 40)

mock_article = MockArticleWithEntities()

print("📋 Original summary with entities:")
print(f"   {mock_article.summary[:100]}...")

result = generate_template_based(mock_article, "trivance_default", "LinkedIn")

print(f"\n✅ Template generation result:")
print(f"   Method: {result['method']}")
print(f"   Character count: {len(result['post'])}")

print(f"\n📝 Generated Post:")
print("-" * 40)
print(result['post'])
print("-" * 40)

# Check if entities were decoded
if "&#38;" in result['post'] or "&#8212;" in result['post']:
    print("❌ HTML entities still present - decoding failed")
else:
    print("✅ HTML entities properly decoded")
