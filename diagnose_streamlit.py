#!/usr/bin/env python3

"""
Streamlit Diagnostic Script
"""

import sys
import os
import subprocess

print("🔍 Streamlit Diagnostic Report")
print("=" * 50)

# Check Python version
print(f"Python version: {sys.version}")

# Check if we're in the right directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# Check if streamlit is in PATH
try:
    result = subprocess.run(['streamlit', '--version'], capture_output=True, text=True, timeout=10)
    print(f"Streamlit version check: {result.returncode}")
    if result.stdout:
        print(f"Streamlit output: {result.stdout.strip()}")
    if result.stderr:
        print(f"Streamlit error: {result.stderr.strip()}")
except subprocess.TimeoutExpired:
    print("❌ Streamlit command timed out")
except FileNotFoundError:
    print("❌ Streamlit command not found in PATH")
except Exception as e:
    print(f"❌ Error running streamlit: {e}")

# Check if streamlit module is importable
try:
    import streamlit
    print(f"✅ Streamlit module imported successfully")
    print(f"   Version: {streamlit.__version__}")
    print(f"   Location: {streamlit.__file__}")
except ImportError as e:
    print(f"❌ Cannot import streamlit: {e}")

# Check if ui/streamlit_app.py exists and is readable
ui_file = "ui/streamlit_app.py"
if os.path.exists(ui_file):
    print(f"✅ {ui_file} exists")
    try:
        with open(ui_file, 'r') as f:
            content = f.read()
        print(f"✅ File is readable ({len(content)} characters)")
        
        # Try to compile it
        try:
            compile(content, ui_file, 'exec')
            print("✅ File compiles without syntax errors")
        except SyntaxError as e:
            print(f"❌ Syntax error: {e}")
            print(f"   Line {e.lineno}: {e.text}")
            
    except Exception as e:
        print(f"❌ Cannot read file: {e}")
else:
    print(f"❌ {ui_file} does not exist")

# Try to run streamlit with python -m
print("\n🧪 Testing streamlit execution methods:")

methods = [
    ['streamlit', 'run', 'ui/streamlit_app.py', '--check-port', 'false'],
    ['python', '-m', 'streamlit', 'run', 'ui/streamlit_app.py', '--check-port', 'false'],
    ['python', '-c', 'import streamlit; print("Import test passed")']
]

for i, method in enumerate(methods, 1):
    print(f"\nMethod {i}: {' '.join(method)}")
    try:
        result = subprocess.run(method, capture_output=True, text=True, timeout=5)
        print(f"  Return code: {result.returncode}")
        if result.stdout:
            print(f"  Stdout: {result.stdout[:200]}")
        if result.stderr:
            print(f"  Stderr: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print("  ⏱️ Timed out (expected for streamlit run)")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n🎯 Recommendations:")
print("1. If streamlit import works, try running manually:")
print("   streamlit run ui/streamlit_app.py")
print("2. If there are syntax errors, fix them first")
print("3. Make sure backend is running on localhost:8000")
print("4. Check firewall/port settings if needed")
