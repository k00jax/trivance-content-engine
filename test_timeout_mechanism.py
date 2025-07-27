"""
Quick timeout test to see if our 15s timeout mechanism works
"""
import sys
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.generator import generate_commentary, USE_GPT, OPENAI_API_KEY

class MockArticle:
    def __init__(self):
        self.title = "Test Article for Timeout"
        self.summary = "This is a test to see if our 15-second timeout works properly."
        self.source = "Test Source"
        self.link = "https://example.com"

print("⏰ Timeout Test")
print("=" * 30)
print(f"USE_GPT: {USE_GPT}")
print(f"API Key: {'✅' if OPENAI_API_KEY else '❌'}")

mock_article = MockArticle()

print(f"\n🚀 Starting generation at {time.strftime('%H:%M:%S')}")
start_time = time.time()

try:
    result = generate_commentary(mock_article, "trivance_default", "LinkedIn")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"🏁 Completed at {time.strftime('%H:%M:%S')} (took {duration:.2f}s)")
    print(f"Method used: {result.get('method', 'unknown')}")
    
    if result.get('method') == 'template':
        print("❌ Used template generation (OpenAI failed or timed out)")
    elif result.get('method') == 'openai_gpt':
        print("✅ Used OpenAI generation successfully!")
    
except Exception as e:
    end_time = time.time()
    duration = end_time - start_time
    print(f"❌ Exception after {duration:.2f}s: {e}")
