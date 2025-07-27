"""
Test the generator with OpenAI GPT enabled
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Test the generator
from services.generator import generate_commentary, USE_GPT, OPENAI_API_KEY

# Mock article object for testing
class MockArticle:
    def __init__(self):
        self.title = "AI Automation Boosts Small Business Efficiency by 40%"
        self.summary = "A recent study shows that small businesses implementing AI automation tools saw a 40% increase in operational efficiency. The research, conducted across 500 companies, found that businesses using AI for routine tasks freed up an average of 15 hours per week for strategic work."
        self.source = "TechCrunch"
        self.link = "https://example.com/article"

print("🤖 Generator OpenAI Test")
print("=" * 40)
print(f"USE_GPT: {USE_GPT}")
print(f"OPENAI_API_KEY configured: {'✅' if OPENAI_API_KEY else '❌'}")

# Test generation
mock_article = MockArticle()

try:
    print("\n🎯 Testing content generation...")
    result = generate_commentary(mock_article, post_style="trivance_default", platform="LinkedIn")
    
    print(f"\n✅ Generation successful!")
    print(f"Method: {result.get('method', 'Unknown')}")
    print(f"Style: {result.get('style_used', 'Unknown')}")
    print(f"Platform: {result.get('platform', 'Unknown')}")
    print(f"Hashtags included: {result.get('hashtags_included', False)}")
    
    print(f"\n📝 Generated Post:")
    print("-" * 40)
    print(result['post'])
    print("-" * 40)
    
except Exception as e:
    print(f"❌ Generation failed: {e}")
    print("This might be normal if OpenAI packages aren't fully installed yet.")
