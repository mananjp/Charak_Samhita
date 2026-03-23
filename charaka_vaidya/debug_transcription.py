"""
Debug script to test Hindi/Gujarati transcription flow
Shows what's happening at each step
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://127.0.0.1:8888"

print("=" * 80)
print("🔍 HINDI/GUJARATI TRANSCRIPTION DEBUG TEST")
print("=" * 80)

# Step 1: Check backend connectivity
print("\n1️⃣ BACKEND CONNECTIVITY")
print("-" * 80)
try:
    health = requests.get(f"{API_BASE}/")
    if health.status_code == 200:
        print(f"✅ Backend responding: {health.json()}")
    else:
        print(f"❌ Backend returned: {health.status_code}")
except Exception as e:
    print(f"❌ Cannot reach backend: {e}")
    print(f"   Make sure FastAPI is running: python api/main.py")
    exit(1)

# Step 2: Check if we can read log output
print("\n2️⃣ LOG OUTPUT RECOMMENDATIONS")
print("-" * 80)
print("""
The transcribe endpoint now logs EVERYTHING. To see it:

Option A: Run FastAPI in foreground
  cd charaka_vaidya
  python -m uvicorn api.main:app --host 127.0.0.1 --port 8888 --reload

Option B: Monitor logs from running instance (if running in background)
  cd charaka_vaidya
  
Windows PowerShell:
  Get-Content logs/app.log -Tail 50 -Wait

Linux/Mac:
  tail -f logs/app.log

Look for these log entries:
  📥 Audio received: [BYTES] bytes
  🎤 Whisper Response:
     language attr: [VALUE]
     language type: [TYPE]
     text: [FIRST 100 CHARS]
  ✅ Normalized language code: [CODE]
""")

# Step 3: Test the language mapping
print("\n3️⃣ LANGUAGE MAPPING TEST")
print("-" * 80)

lang_map = {
    # === ISO 639-1 codes (what Whisper actually returns) ===
    "en": "en", 
    "hi": "hi", 
    "gu": "gu",
    # === Full language names (lowercase) ===
    "english": "en", 
    "hindi": "hi", 
    "gujarati": "gu",
    # === BCP-47 and regional variants ===
    "en-in": "en", "en-in-x-twain": "en",
    "en-us": "en", 
    "en-gb": "en",
    "hi-in": "hi",
    "gu-in": "gu",
    # === Legacy/alternate formats (fallback) ===
    "indic_en": "en",
    "indic_hi": "hi",
    "indic_gu": "gu",
}

test_detections = [
    "en",              # Expected from English
    "hi",              # Expected from Hindi
    "gu",              # Expected from Gujarati
    "hindi",           # Possible from Whisper
    "gujarati",        # Possible from Whisper
    "english",         # Possible from Whisper
    "hi-in",           # BCP-47 variant
    "gu-in",           # BCP-47 variant
    "Hindi",           # Capitalized (if Whisper returns this)
    "Gujarati",        # Capitalized
    "hi-IN",           # Mixed case
    "Unknown",         # Should NOT match
]

print("Testing language mapping:")
for detected in test_detections:
    detected_lower = detected.lower().strip()
    mapped = lang_map.get(detected_lower)
    status = "✅" if mapped else "❌"
    print(f"  {status} '{detected}' → '{detected_lower}' → '{mapped}'")

# Step 4: What to check
print("\n4️⃣ WHAT TO CHECK")
print("-" * 80)
print("""
When testing Hindi/Gujarati voice recording:

1. BACKEND LOGS should show:
   - 📥 Audio received message
   - 🎤 Whisper Response with exact language value
   - ✅ Normalized language code
   
2. STREAMLIT UI should show:
   - "🎙️ Detected lang: [CODE]" message
   - Transcribed text
   - Language should auto-switch in UI
   
3. ISSUES TO WATCH FOR:
   - ⚠️ "Unknown language code" warning
   - ❌ Error messages in API response
   - No language auto-switch happening
   - Wrong language being used for TTS output

4. SOLUTIONS:
   - If mapping fails: Add new format to lang_map
   - If Whisper fails: Check audio quality/format (should be WAV, mono, 16kHz)
   - If lang doesn't switch: Check if lang_pinned is True
   - If TTS wrong: Verify BCP-47 codes in speak_button.py
""")

# Step 5: Check logs for errors
print("\n5️⃣ HOW TO FIND THE PROBLEM")
print("-" * 80)
print("""
The most common issues with Hindi/Gujarati transcription:

ISSUE 1: Wrong Audio Format
  - Streamlit audio_input() might record in wrong format
  - Solution: Check logs for content-type and file size
  
ISSUE 2: Language Code Mapping Missing
  - Whisper returns format not in lang_map
  - Solution: Check what Whisper returns in logs, add to mapping
  
ISSUE 3: Session State Not Updating
  - Language detected but UI not switching
  - Solution: Check if lang_pinned=True, check st.rerun() is called
  
ISSUE 4: Groq API Key Issue
  - Transcription failing silently
  - Solution: Check if API key in .env file is valid

ISSUE 5: Whisper Not Supporting Language
  - Groq Whisper might not support Hindi/Gujarati
  - Solution: Check Groq API documentation for supported languages
  - Workaround: Use language="hi" or language="gu" explicitly
""")

print("\n" + "=" * 80)
print("📝 ACTION ITEMS:")
print("=" * 80)
print("""
1. ✅ Run FastAPI backend in foreground (for log visibility)
   cd charaka_vaidya
   python -m uvicorn api.main:app --host 127.0.0.1 --port 8888

2. ✅ Open Streamlit app: http://localhost:8501

3. ✅ Go to "Chat" page, select "Voice Input" tab

4. ✅ Record in Hindi (or Gujarati)

5. ✅ Look at FastAPI terminal for these logs:
   - 📥 Audio received
   - 🎤 Whisper Response:
       language attr: [THIS IS THE KEY!]

6. ✅ Report what this value is. Common possibilities:
   - "hi" or "en" (supported, should work)
   - "hindi" (needs mapping, already added)
   - Something else (needs investigation)

7. ✅ Check Streamlit UI for error messages

8. ✅ Verify logs for language mapping and session state details
""")

print("\n" + "=" * 80)
