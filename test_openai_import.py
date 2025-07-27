"""
Simple test to check OpenAI package import
"""
try:
    import openai
    print("✅ OpenAI package imported successfully")
    print(f"OpenAI version: {openai.__version__}")
    
    # Test client creation
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            client = openai.OpenAI(api_key=api_key)
            print("✅ OpenAI client created successfully")
        else:
            print("❌ No API key found")
            
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        
except ImportError as e:
    print(f"❌ Cannot import openai: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
