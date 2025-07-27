"""
Isolated OpenAI test to debug the specific failure
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.generator import generate_with_openai, USE_GPT, OPENAI_API_KEY

class MockArticle:
    def __init__(self):
        self.title = "Test OpenAI Direct Call"
        self.summary = "This is a simple test to verify OpenAI API functionality with minimal complexity."
        self.source = "Test"
        self.link = "https://example.com"

print("🔍 Isolated OpenAI Test")
print("=" * 40)
print(f"USE_GPT: {USE_GPT}")
print(f"OPENAI_API_KEY configured: {'✅' if OPENAI_API_KEY else '❌'}")

if not USE_GPT:
    print("❌ OpenAI is disabled in environment")
    exit(1)

if not OPENAI_API_KEY:
    print("❌ No OpenAI API key found")
    exit(1)

mock_article = MockArticle()

print("\n🎯 Calling generate_with_openai directly...")
try:
    result = generate_with_openai(mock_article, "trivance_default", "LinkedIn")
    
    print(f"\n📋 Raw Result:")
    print(f"   Method: {result.get('method', 'MISSING')}")
    print(f"   Error: {result.get('error', 'None')}")
    print(f"   Fallback: {result.get('fallback', 'False')}")
    print(f"   Post length: {len(result.get('post', '')) if result.get('post') else 0}")
    
    if result.get('post'):
        print(f"\n📝 Generated Post (first 200 chars):")
        print(f"   {result['post'][:200]}...")
    
except Exception as e:
    print(f"❌ Exception during direct call: {e}")
    import traceback
    traceback.print_exc()
