"""
Minimal OpenAI test with explicit timeout
"""
import signal
import os
from dotenv import load_dotenv

load_dotenv()

def timeout_handler(signum, frame):
    raise TimeoutError("API call timed out")

def test_openai_minimal():
    try:
        import openai
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ No API key")
            return
        
        print("🔧 Creating client...")
        client = openai.OpenAI(api_key=api_key)
        
        print("🚀 Making minimal API call...")
        
        # Set a signal alarm for 30 seconds
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Say 'Hello from Trivance AI' in exactly 4 words."}
                ],
                max_tokens=10,
                temperature=0
            )
            
            # Cancel the alarm
            signal.alarm(0)
            
            text = response.choices[0].message.content.strip()
            print(f"✅ Success: '{text}'")
            print(f"📊 Tokens: {response.usage.total_tokens if response.usage else 'unknown'}")
            
        except TimeoutError:
            print("❌ API call timed out after 30 seconds")
        except Exception as api_error:
            signal.alarm(0)  # Cancel alarm
            print(f"❌ API error: {api_error}")
            
    except ImportError:
        print("❌ OpenAI library not available")
    except Exception as e:
        print(f"❌ General error: {e}")

if __name__ == "__main__":
    print("🧪 Minimal OpenAI Timeout Test")
    print("=" * 30)
    test_openai_minimal()
