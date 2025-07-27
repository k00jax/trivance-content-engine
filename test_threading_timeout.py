"""
Windows-compatible OpenAI test with threading timeout
"""
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

def test_openai_with_timeout():
    result = {"success": False, "response": None, "error": None}
    
    def api_call():
        try:
            import openai
            
            api_key = os.getenv("OPENAI_API_KEY")
            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Say 'Hello Trivance' in 2 words."}
                ],
                max_tokens=5,
                temperature=0
            )
            
            result["success"] = True
            result["response"] = response.choices[0].message.content.strip()
            
        except Exception as e:
            result["error"] = str(e)
    
    print("🧪 Windows OpenAI Timeout Test")
    print("=" * 30)
    print("🚀 Starting API call in thread...")
    
    # Start the API call in a separate thread
    thread = threading.Thread(target=api_call)
    thread.daemon = True
    thread.start()
    
    # Wait for up to 30 seconds
    thread.join(timeout=30)
    
    if thread.is_alive():
        print("❌ API call timed out after 30 seconds")
        print("🔍 This suggests a network/firewall issue")
        return False
    elif result["success"]:
        print(f"✅ Success: '{result['response']}'")
        return True
    elif result["error"]:
        print(f"❌ API Error: {result['error']}")
        return False
    else:
        print("❌ Unknown failure")
        return False

if __name__ == "__main__":
    success = test_openai_with_timeout()
    
    if not success:
        print("\n💡 Troubleshooting suggestions:")
        print("   1. Check internet connection")
        print("   2. Check firewall/proxy settings")
        print("   3. Verify API key has credits")
        print("   4. Try a different network")
