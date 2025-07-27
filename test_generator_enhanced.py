"""
Test script for improved post generator with style control and content accuracy.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.generator import (
    generate_commentary, 
    extract_key_insights,
    generate_hashtags,
    get_available_styles,
    STYLE_EXAMPLES
)

# Mock article object for testing
class MockArticle:
    def __init__(self, title, summary, source, link=""):
        self.title = title
        self.summary = summary
        self.source = source
        self.link = link

def test_key_insights_extraction():
    """Test the key insights extraction functionality."""
    print("🔍 Testing Key Insights Extraction...")
    
    test_summaries = [
        "A new study shows that 85% of small businesses increased productivity by 40% after implementing AI automation tools. The research found that companies focusing on workflow optimization see the best results.",
        'OpenAI announced its latest ChatGPT update will include "advanced reasoning capabilities" and improved integration with business tools. The company revealed plans to expand enterprise features.',
        "Business leaders report mixed results with AI adoption. While 60% see operational improvements, many struggle with implementation challenges and team training requirements."
    ]
    
    for i, summary in enumerate(test_summaries, 1):
        insights = extract_key_insights(summary)
        print(f"\nSummary {i}: {summary[:60]}...")
        print(f"Extracted insights: {insights}")
        print("-" * 60)

def test_style_variations():
    """Test different post styles with the same article."""
    print("\n✍️ Testing Style Variations...")
    
    sample_article = MockArticle(
        title="AI Tools Boost Small Business Efficiency by 40%",
        summary="A comprehensive study of 500 small businesses found that companies using AI automation tools reported 40% higher efficiency and 25% cost savings. The research revealed that businesses focusing on workflow optimization rather than wholesale transformation achieved the best results. 'The key is starting small and scaling gradually,' said lead researcher Dr. Sarah Chen.",
        source="Business Technology Report",
        link="https://example.com/ai-efficiency-study"
    )
    
    styles = ["consultative", "punchy", "casual"]
    
    for style in styles:
        print(f"\n{'='*20} {style.upper()} STYLE {'='*20}")
        print(f"Description: {STYLE_EXAMPLES[style]['description']}")
        print("-" * 60)
        
        result = generate_commentary(sample_article, post_style=style)
        
        print("Generated Post:")
        print(result["post"])
        print()
        print(f"Method: {result.get('method', 'unknown')}")
        print(f"Key insights found: {result.get('key_insights', [])}")
        print(f"Specific detail used: {result.get('specific_detail', 'none')[:100]}...")
        print("="*60)

def test_content_accuracy():
    """Test that generated content actually uses article information."""
    print("\n🎯 Testing Content Accuracy...")
    
    # Article with specific stats and quotes
    specific_article = MockArticle(
        title="ChatGPT Usage Jumps 300% Among Marketing Teams",
        summary='New data from MarketingAI Corp shows ChatGPT usage in marketing departments increased 300% in Q4 2024. "We\'re seeing unprecedented adoption rates," said CEO Mike Rodriguez. The study found that 78% of teams use AI for content creation, while 45% leverage it for campaign strategy. Companies report saving an average of 15 hours per week on routine tasks.',
        source="MarketingAI Corp",
        link="https://example.com/marketing-ai-study"
    )
    
    result = generate_commentary(specific_article, post_style="consultative")
    
    print("Original Summary:")
    print(specific_article.summary)
    print("\nGenerated Post:")
    print(result["post"])
    print("\nContent Analysis:")
    print(f"Key insights extracted: {result.get('key_insights', [])}")
    print(f"Specific detail used: {result.get('specific_detail', 'none')}")
    
    # Check if specific numbers or quotes are referenced
    post_content = result["post"].lower()
    original_summary = specific_article.summary.lower()
    
    # Look for key numbers
    numbers_in_summary = ["300%", "78%", "45%", "15 hours"]
    numbers_found = [num for num in numbers_in_summary if num.lower() in post_content]
    
    print(f"\nNumbers from summary found in post: {numbers_found}")
    
    # Check for quote reference
    has_quote_reference = "rodriguez" in post_content or "unprecedented" in post_content
    print(f"Quote/authority referenced: {has_quote_reference}")

def test_hashtag_relevance():
    """Test hashtag generation accuracy."""
    print("\n🏷️ Testing Hashtag Generation...")
    
    test_cases = [
        ("ChatGPT Transforms Customer Service", "Automation and AI chatbots improve business productivity"),
        ("Startup Uses Machine Learning for Growth", "Data analytics and ML help small business scale operations"),
        ("Executive Leadership in Digital Transformation", "CEOs embrace technology strategy for competitive advantage")
    ]
    
    for title, summary in test_cases:
        hashtags = generate_hashtags(title, summary)
        print(f"Title: {title}")
        print(f"Summary: {summary}")
        print(f"Generated hashtags: {hashtags}")
        print("-" * 50)

if __name__ == "__main__":
    print("🧪 Enhanced Post Generator Test Suite")
    print("=" * 70)
    
    print(f"Available styles: {list(get_available_styles().keys())}")
    print()
    
    test_key_insights_extraction()
    test_style_variations()
    test_content_accuracy()
    test_hashtag_relevance()
    
    print("\n✅ Enhanced testing complete!")
    print("\nNext steps:")
    print("1. Start FastAPI server: uvicorn app.main:app --reload")
    print("2. Test style control in Streamlit UI")
    print("3. Verify content accuracy with real articles")
    print("4. Check that post styles produce noticeably different outputs")
