"""
Test script for the updated Trivance AI content generator.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.generator import generate_commentary, generate_hashtags

# Mock article object for testing
class MockArticle:
    def __init__(self, title, summary, source, link=""):
        self.title = title
        self.summary = summary
        self.source = source
        self.link = link

def test_hashtag_generation():
    """Test hashtag generation functionality."""
    print("🔍 Testing Hashtag Generation...")
    
    test_cases = [
        ("ChatGPT transforms business automation", "AI and machine learning revolutionize workflows"),
        ("Small business strategy with AI", "Entrepreneurship meets artificial intelligence"),
        ("Data analytics for startups", "Business intelligence and productivity gains")
    ]
    
    for title, summary in test_cases:
        hashtags = generate_hashtags(title, summary)
        print(f"Title: {title}")
        print(f"Hashtags: {hashtags}")
        print("-" * 50)

def test_content_generation():
    """Test content generation with sample article."""
    print("\n📝 Testing Content Generation...")
    
    sample_article = MockArticle(
        title="AI Adoption Grows 300% Among SMBs in 2024",
        summary="New research shows small and medium businesses are rapidly adopting AI tools for customer service, content creation, and data analysis. The study reveals that companies using AI report 40% higher productivity and 25% cost savings.",
        source="Business Tech Weekly",
        link="https://example.com/ai-adoption-study"
    )
    
    result = generate_commentary(sample_article)
    
    print("Generated Post:")
    print("=" * 60)
    print(result["post"])
    print("=" * 60)
    print(f"Method: {result.get('method', 'unknown')}")
    print(f"Hashtags: {result.get('hashtags', 'none')}")

if __name__ == "__main__":
    test_hashtag_generation()
    test_content_generation()
    
    print("\n✅ Testing complete!")
    print("\nTo enable GPT generation:")
    print("1. pip install openai")
    print("2. set USE_OPENAI_GPT=true")
    print("3. set OPENAI_API_KEY=your-key-here")
