"""
Minimal OpenAI test
"""
import os
from dotenv import load_dotenv
load_dotenv()

import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Making simple API call...")
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=5
    )
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"Error: {e}")
