import os

def check_openai_environment():
    use_gpt = os.getenv("USE_OPENAI_GPT", "false").lower()
    api_key = os.getenv("OPENAI_API_KEY")
    
    print("🔍 Trivance AI OpenAI Config Check")
    print("----------------------------------")
    print(f"USE_OPENAI_GPT: {use_gpt}")
    print(f"OPENAI_API_KEY set: {'✅ Yes' if api_key else '❌ No'}")

    if use_gpt == "true" and api_key:
        print("✅ OpenAI generation should be ENABLED.")
    else:
        print("⚠️  OpenAI generation is DISABLED. Check your environment variables.")

if __name__ == "__main__":
    check_openai_environment()
