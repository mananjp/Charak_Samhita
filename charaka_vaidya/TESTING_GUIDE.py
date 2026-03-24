"""
TESTING GUIDE: Hindi/Gujarati Transcription Troubleshooting
============================================================

This guide walks through diagnosing why Hindi/Gujarati transcription isn't working.
"""

# STEP 1: Verify Backend is Running
print("=" * 80)
print("STEP 1: VERIFY BACKEND IS RUNNING")
print("=" * 80)
print("""
Check if FastAPI is running on port 8888:
  PowerShell: netstat -ano | findstr :8888
  
If running, you should see output like:
  TCP    127.0.0.1:8888    0.0.0.0:0    LISTENING    [PID]

If not running, the backend was just started. Wait 5 seconds for it to be ready.
""")

# STEP 2: Test Backend Connectivity
print("\n" + "=" * 80)
print("STEP 2: TEST BACKEND CONNECTIVITY")
print("=" * 80)

import requests
import time

print("Testing backend health endpoint...")
try:
    response = requests.get("http://127.0.0.1:8888/", timeout=2)
    print(f"✅ Backend responding!")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend on port 8888")
    print("   Make sure FastAPI is running (check Step 1)")
except Exception as e:
    print(f"⚠️ Unexpected error: {e}")

# STEP 3: Understanding the Transcription Problem
print("\n" + "=" * 80)
print("STEP 3: UNDERSTANDING THE PROBLEM")
print("=" * 80)
print("""
The most likely causes for Hindi/Gujarati not working:

┌─────────────────────────────────────────────────────────────────┐
│ PROBLEM A: Whisper Returns Unexpected Language Code             │
├─────────────────────────────────────────────────────────────────┤
│ Issue: Groq Whisper returns a language format not in lang_map   │
│ Evidence: You see transcription but UI doesn't switch language  │
│ Solution: Check backend logs for exact value Whisper returns    │
│           Update lang_map with new format                       │
│ Likelihood: MEDIUM                                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PROBLEM B: Audio Format Not Recognized by Whisper               │
├─────────────────────────────────────────────────────────────────┤
│ Issue: Streamlit audio_input() records in format Whisper can't  │
│        properly transcribe non-English audio                    │
│ Evidence: Transcription fails or returns empty text             │
│ Solution: Check audio format in logs (should be audio/wav)      │
│           Verify audio size (should be >1KB)                    │
│ Likelihood: HIGH                                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PROBLEM C: Groq API Key Issues                                  │
├─────────────────────────────────────────────────────────────────┤
│ Issue: GROQ_API_KEY not valid or insufficient permissions       │
│ Evidence: API returns 401 or 403 error                          │
│ Solution: Verify API key is correct in .env file               │
│           Test with English first (confirm basic API works)     │
│ Likelihood: LOW (system was working for English)                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PROBLEM D: Language Pinned in UI                                │
├─────────────────────────────────────────────────────────────────┤
│ Issue: User clicked "Language Preference" which pinned language │
│ Evidence: Language doesn't auto-switch even when detected       │
│ Solution: Look for "lang_pinned" setting in Streamlit sidebar   │
│           Uncheck if detected                                   │
│ Likelihood: MEDIUM                                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PROBLEM E: Whisper Model Limitations                            │
├─────────────────────────────────────────────────────────────────┤
│ Issue: whisper-large-v3 has limitations with certain languages  │
│ Evidence: Always returns English transcription for Hindi/Gu    │
│ Solution: Explicitly specify language in Whisper call           │
│           Use: language="hi" or language="gu"                   │
│ Likelihood: LOW (Whisper supports 99+ languages)                │
└─────────────────────────────────────────────────────────────────┘
""")

# STEP 4: How to Diagnose
print("\n" + "=" * 80)
print("STEP 4: HOW TO DIAGNOSE (DETAILED INSTRUCTIONS)")
print("=" * 80)
print("""
FOLLOW THESE STEPS EXACTLY:

1. Open your browser and go to: http://localhost:8501
   
2. Navigate to "Consult Charaka Vaidya" → "Chat" page
   
3. Click on the "Voice Input" tab
   
4. RECORD A 3-5 SECOND AUDIO IN HINDI (or Gujarati)
   - Speak naturally: "नमस्ते, मुझे अपनी सेहत के बारे में पूछना है"
   - (Or Gujarati: "નમસ્તે, હું મારા આરોગ્ય વિશે પૂછવા માંગું છું")
   
5. IMMEDIATELY CHECK THE FASTAPI BACKEND LOGS
   ➜ Look for the pattern:
   
     📥 Audio received: [NUMBER] bytes, type: [TYPE], filename: [NAME]
     🎤 Whisper Response:
        language attr: [THIS IS KEY - WHAT DOES IT SAY?]
        language type: [TYPE]
        text: [FIRST 100 CHARS]
             └─ This should be in Hindi/Gujarati
     ✅ Normalized language code: [NORMALIZED]
   
6. ALSO CHECK STREAMLIT OUTPUT
   It should show:
     - "🎙️ Detected lang: [CODE]"
     - "Transcribed: [Your Hindi/Gujarati text]"
     - UI should switch to detected language
   
7. REPORT WHAT YOU SEE
   - What exact value appears in "language attr:"
   - Does the text show correctly in Hindi/Gujarati?
   - Does the UI language switch?
   - Any error messages?
""")

# STEP 5: Quick Diagnostic Checklist
print("\n" + "=" * 80)
print("STEP 5: QUICK DIAGNOSTIC CHECKLIST")
print("=" * 80)
print("""
Mark each with YES or NO:

□ Backend is running on 8888          (FastAPI terminal visible/logs flowing)
□ Backend responds to health check    (GET / returns status: ok)
□ Audio was recorded successfully     (📥 Audio received log appears)
□ Audio was sent to backend           (No connection errors)
□ Whisper returned some value         (🎤 Whisper Response log appears)
□ Transcribed text looks correct      (Text is in Hindi/Gujarati not English)
□ Language code was detected          (language attr: shows hi or gu)
□ Mapping was applied correctly       (✅ Normalized language code shows hi or gu)
□ UI language changed                 (Page switched to Hindi/Gujarati layout)
□ TTS played in correct language      (Listen button used correct voice)

WHAT THIS MEANS:
- All YES:      System is working perfectly! 🎉
- Some NO:      Check the DIAGNOSIS section below for that specific NO
- Many NO:      Skip to ADVANCED DIAGNOSTICS section
""")

# STEP 6: Diagnosis by Symptom
print("\n" + "=" * 80)
print("STEP 6: DIAGNOSIS BY SYMPTOM")
print("=" * 80)
print("""
IF PROBLEM: "Audio received" log doesn't appear
─────────────────────────────────────────────────
→ Backend might not be running or logs not visible
→ Check: cd charaka_vaidya && python -m uvicorn api.main:app --port 8888
→ Should see: "Uvicorn running on http://127.0.0.1:8888"

IF PROBLEM: "Whisper Response" log doesn't appear
──────────────────────────────────────────────────
→ Transcription request failed before reaching Whisper
→ Likely cause: File upload format issue (Problem B)
→ Check: Is content-type showing "audio/wav" in "Audio received" log?
→ Fix: Reinstall streamlit: pip install --upgrade streamlit

IF PROBLEM: Text returned is in ENGLISH instead of Hindi/Gujarati
──────────────────────────────────────────────────────────────────
→ Whisper detected language incorrectly
→ Likely cause: Audio format or quality issue (Problem B)
→ Try: Record longer (5+ seconds), speak clearly, no background noise
→ Fix (if repeatedly fails): Explicitly set language in transcribe.py
        Change: language=None
        To:     language="hi"  # for Hindi

IF PROBLEM: Language code not recognized / "Unknown language code" warning
──────────────────────────────────────────────────────────────────────────
→ Whisper returned format not in lang_map (Problem A)
→ Solution: 
   1. Check what Whisper returned in logs
   2. Add mapping to lang_map in voice_button.py
   3. Look for pattern in normalized language code

IF PROBLEM: UI doesn't auto-switch even with correct language detected
───────────────────────────────────────────────────────────────────────
→ Either lang is pinned OR Streamlit didn't rerun
→ Check: Is there a checkbox "Pin Language" checked in sidebar?
→ Try: Uncheck it, then record again
→ Also check logs for: "Lang pinned" or "Language pinned" message

IF PROBLEM: TTS plays in wrong language even after UI switches
──────────────────────────────────────────────────────────────
→ Issue in speak_button.py BCP-47 code mapping
→ Check: Open browser Developer Tools (F12) → Console
→ Look for: Speech synthesis language code being used
→ Fix: Verify get_bcp47() returns correct "hi-IN" or "gu-IN"
""")

# STEP 7: Advanced Diagnostics
print("\n" + "=" * 80)
print("STEP 7: ADVANCED DIAGNOSTICS")
print("=" * 80)
print("""
If basic diagnostics don't work, try these advanced steps:

1. CHECK RAW API RESPONSE
   ────────────────────────
   Create a Python script:
   
   import requests
   
   # Create a test audio file (WAV needs real audio data)
   # For now, just test the endpoint exists:
   response = requests.post(
       "http://127.0.0.1:8888/transcribe",
       files={"file": ("test.wav", b"fake audio", "audio/wav")},
       timeout=30
   )
   print(f"Status: {response.status_code}")
   print(f"Response: {response.json()}")

2. TEST WHISPER DIRECTLY
   ────────────────────────
   Create: test_whisper_direct.py
   
   from groq import Groq
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   client = Groq(api_key=os.getenv("GROQ_API_KEY"))
   
   # Play with different settings
   print("Testing Whisper with language=None (auto-detect)...")
   print("  [Requires actual audio file]")
   
   print("\\nSupported Groq Whisper languages:")
   print("  'en' (English), 'hi' (Hindi), 'gu' (Gujarati), etc.")

3. CHECK STREAMLIT LOGS
   ────────────────────────
   Streamlit logs are at: ~/.streamlit/logs/streamlit_logs/
   
   Or run with debug:
   streamlit run pages/1_Chat.py --logger.level=debug

4. ENABLE DEBUG MODE IN voice_button.py
   ─────────────────────────────────────
   Add st.write() calls to show internal state:
   
   st.write(f"DEBUG: detected_language = {detected}")
   st.write(f"DEBUG: lang_map result = {mapped}")
   st.write(f"DEBUG: current session lang = {st.session_state['lang']}")
""")

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("""
1. Ensure FastAPI backend is running (check port 8888)
2. Go to http://localhost:8501 and test voice recording
3. Record in Hindi or Gujarati
4. Check FastAPI logs for the exact language code Whisper returns
5. Report the value in "language attr:" field
6. I'll help debug from there

The enhanced logging will help us pinpoint exactly where the issue is!
""")
print("=" * 80)
