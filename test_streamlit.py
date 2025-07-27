#!/usr/bin/env python3

"""
Test Streamlit app imports to identify issues
"""

import sys
import os

print("🔍 Testing Streamlit App Imports")
print("=" * 40)

try:
    import streamlit as st
    print("✅ streamlit import successful")
except Exception as e:
    print(f"❌ streamlit import failed: {e}")

try:
    import requests
    print("✅ requests import successful")
except Exception as e:
    print(f"❌ requests import failed: {e}")

print("\n🔍 Testing Streamlit App Syntax")
print("=" * 40)

try:
    # Try to compile the streamlit app without running it
    with open('ui/streamlit_app.py', 'r') as f:
        code = f.read()
    
    compile(code, 'ui/streamlit_app.py', 'exec')
    print("✅ Streamlit app syntax is valid")
    
    # Count lines of code
    lines = len(code.split('\n'))
    print(f"✅ File has {lines} lines")
    
except SyntaxError as e:
    print(f"❌ Syntax error in streamlit app: {e}")
    print(f"   Line {e.lineno}: {e.text}")
except Exception as e:
    print(f"❌ Error reading streamlit app: {e}")

print("\n🔍 API Configuration Test")
print("=" * 40)

# Test if the API URL is reachable
try:
    import requests
    response = requests.get("http://localhost:8000", timeout=2)
    print("✅ Backend API is running")
except requests.exceptions.ConnectionError:
    print("⚠️  Backend API is not running (expected if not started)")
except Exception as e:
    print(f"❌ API test error: {e}")

print("\n🚀 Streamlit Test Complete")
print("If syntax is valid, try running:")
print("  streamlit run ui/streamlit_app.py")
print("  OR start backend first: python -m uvicorn app.main:app --reload")
