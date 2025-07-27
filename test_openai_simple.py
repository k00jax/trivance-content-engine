"""
Focused OpenAI API test with timeout and better error handling
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Test environment variables
api_key = os.getenv("OPENAI_API_KEY")
use_gpt = os.getenv("USE_OPENAI_GPT", "false").lower() == "true"

print(f"USE_OPENAI_GPT: {use_gpt}")
print(f"API Key format: {api_key[:10]}...{api_key[-10:] if api_key and len(api_key) > 20 else 'Invalid'}")

if not api_key:
    print("❌ No API key found")
    sys.exit(1)

if not api_key.startswith("sk-"):
    print("❌ API key doesn't start with 'sk-'")
    sys.exit(1)

try:
    import openai
    print("✅ OpenAI imported successfully")
    
    client = openai.OpenAI(api_key=api_key)
    print("✅ Client created")
    
    # Test simple completion with timeout
    print("🧪 Testing API call...")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use cheaper model for testing
        messages=[
            {"role": "user", "content": "Say 'Hello from OpenAI' in exactly 3 words."}
        ],
        max_tokens=10,
        timeout=15  # 15 second timeout
    )
    
    result = response.choices[0].message.content.strip()
    print(f"✅ API Response: {result}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
