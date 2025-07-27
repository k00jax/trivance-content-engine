🔧 STREAMLIT TROUBLESHOOTING GUIDE
==========================================

## ❗ Common Issues & Solutions

### 1. Missing Dependencies
✅ **FIXED**: Dependencies are now installed
- streamlit 1.45.0
- openai 1.97.1  
- fastapi, uvicorn, requests, etc.

### 2. Backend Not Running
❌ **LIKELY ISSUE**: Streamlit app expects API at localhost:8000

**Solution**: Start the backend first
```bash
python -m uvicorn app.main:app --reload
```

### 3. Manual Streamlit Start
If automatic start fails, try these methods:

**Method 1** (Recommended):
```bash
streamlit run ui/streamlit_app.py
```

**Method 2** (Alternative):
```bash
python -m streamlit run ui/streamlit_app.py
```

**Method 3** (Debug mode):
```bash
streamlit run ui/streamlit_app.py --server.port 8501 --server.headless false
```

### 4. Quick Fix Script
Use the provided batch file:
```bash
start_apps.bat
```

This starts both backend and frontend automatically.

## 🧪 Testing Steps

### Step 1: Start Backend
```bash
cd "c:\Users\black\OneDrive\Desktop\Trivance AI\trivance-content-engine"
python -m uvicorn app.main:app --reload
```

Wait for: "Uvicorn running on http://127.0.0.1:8000"

### Step 2: Test Backend
Open browser to: http://localhost:8000/docs
You should see FastAPI documentation.

### Step 3: Start Frontend
In new terminal:
```bash
streamlit run ui/streamlit_app.py
```

Expected output:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Step 4: Access Application
Open browser to: http://localhost:8501

## 🔍 If Still Not Working

### Check Python Environment
```bash
python --version
pip list | findstr streamlit
```

### Check Port Availability
```bash
netstat -ano | findstr :8501
netstat -ano | findstr :8000
```

### Run Diagnostics
```bash
python diagnose_streamlit.py
```

## 📋 Expected UI Features

Once working, you should see:

### Generate Post Tab:
- ✅ Grouped article dropdowns by RSS source
- ✅ "Choose Most Relevant Article" button  
- ✅ Collapsible sections with scores
- ✅ Article selection highlighting
- ✅ Clean layout with metrics

### Debug Features:
- ✅ Enhanced logging when generating posts
- ✅ Template pattern detection
- ✅ Fallback reason tracking
- ✅ OpenAI vs Template method validation

## 🚀 Quick Start Commands

**Option 1** - Automatic (recommended):
```bash
start_apps.bat
```

**Option 2** - Manual:
```bash
# Terminal 1 (Backend)
python -m uvicorn app.main:app --reload

# Terminal 2 (Frontend) 
streamlit run ui/streamlit_app.py
```

**Option 3** - Debug mode:
```bash
# Set debug mode first
set DEBUG_GPT_RESPONSE=true

# Then start normally
start_apps.bat
```

## ✅ Verification Checklist

- [ ] Backend running on localhost:8000
- [ ] Frontend running on localhost:8501  
- [ ] Can fetch articles in UI
- [ ] Articles grouped by RSS source
- [ ] Can select articles by clicking
- [ ] Can generate posts
- [ ] Debug logging works (check console)

The UI improvements are ready - the issue is likely just getting Streamlit started properly!
