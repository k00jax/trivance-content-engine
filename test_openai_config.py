"""
Quick test to verify OpenAI GPT configuration is working
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check configuration
use_gpt = os.getenv("USE_OPENAI_GPT", "false").lower() == "true"
api_key = os.getenv("OPENAI_API_KEY")

print("🔧 OpenAI GPT Configuration Test")
print("=" * 40)
print(f"USE_OPENAI_GPT: {use_gpt}")
print(f"OPENAI_API_KEY: {'✅ Set' if api_key else '❌ Missing'}")
print(f"API Key length: {len(api_key) if api_key else 0} characters")

if use_gpt and api_key:
    print("\n✅ Configuration is correct! OpenAI GPT is enabled.")
    
    # Test basic import
    try:
        import openai
        print("✅ OpenAI library is installed and importable")
        
        # Test client initialization
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
        
    except ImportError:
        print("❌ OpenAI library not installed. Run: pip install openai")
    except Exception as e:
        print(f"⚠️  OpenAI client issue: {e}")
        
else:
    print("\n❌ Configuration issue:")
    if not use_gpt:
        print("   - USE_OPENAI_GPT is not set to 'true'")
    if not api_key:
        print("   - OPENAI_API_KEY is missing")
