"""
Test script to see what Whisper actually returns for different languages
"""
import os
import sys
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    print("❌ GROQ_API_KEY not set in .env")
    sys.exit(1)

client = Groq(api_key=API_KEY)

# Test with sample audio files if they exist
test_files = [
    ("test_hindi.wav", "hindi"),
    ("test_gujarati.wav", "gujarati"),
    ("test_english.wav", "english"),
]

print("=" * 80)
print("🔍 WHISPER LANGUAGE DETECTION TEST")
print("=" * 80)

# Since we don't have actual audio files, let's test with the API directly
# by creating a simple test with generated audio data

# First, let's check what the API returns by looking at response structure
print("\n📋 Groq Whisper API Response Structure Analysis:")
print("-" * 80)

print("""
When calling Groq Whisper with language=None (auto-detect):
  
  response = client.audio.transcriptions.create(
      file=(filename, audio_bytes, content_type),
      model="whisper-large-v3",
      response_format="verbose_json",
      language=None,
      temperature=0.0
  )
  
Expected response attributes:
  - response.text: The transcribed text
  - response.language: The detected language CODE (e.g., "en", "hi", "gu", "pt", etc.)
  
According to Groq docs:
  - Language should be ISO 639-1 code (2-letter code)
  - For Hindi: "hi"
  - For Gujarati: "gu"  
  - For English: "en"
""")

print("\n⚠️  POTENTIAL ISSUES:")
print("-" * 80)

print("""
1. **Language Code Format Issue**
   - Whisper may return full language names ("Hindi", "Gujarati") instead of codes ("hi", "gu")
   - The lang_map in voice_button.py needs to handle both formats
   
   Current mapping (with .lower()):
   ✓ "en" → "en"
   ✓ "hindi" → "hi" (assuming Whisper returns lowercase)
   ✓ "gujarati" → "gu" (assuming Whisper returns lowercase)
   ✗ BUT if Whisper returns "Hindi" or "Gujarati" (capitalized), mapping fails!
   
2. **Missing Language Code Variants**
   - Whisper might return different formats not yet in the mapping
   
3. **Session State Not Updated**
   - Even if language is detected, session state might not be updating properly
   
4. **API Response Content-Type**
   - Audio format might be causing transcription to fail for non-English
""")

print("\n✅ RECOMMENDED FIXES:")
print("-" * 80)

improved_mapping = {
    # Direct codes (lowercase)
    "en": "en", "hi": "hi", "gu": "gu",
    # Text names (lowercase) 
    "english": "en", "hindi": "hi", "gujarati": "gu",
    # BCP-47 and regional variants
    "en-us": "en", "en-gb": "en", "en-in": "en",
    "hi-in": "hi", "hi": "hi",
    "gu-in": "gu", "gu": "gu",
    # Full names with variants (to be lowercased in code)
    "english (en-us)": "en", "english (united states)": "en",
    "hindi": "hi", "hindi (india)": "hi",
    "gujarati": "gu", "gujarati (india)": "gu",
}

print("Enhanced lang_map to handle:")
for key, value in sorted(improved_mapping.items()):
    print(f"  '{key}' → '{value}'")

print("\n🔧 DEBUGGING NEXT STEPS:")
print("-" * 80)
print("""
1. Add logging to transcribe.py endpoint:
   - Log the full response object from Whisper
   - Log the detected language value and its type
   - Log what value is being returned to frontend
   
2. Add logging to voice_button.py:
   - Log the exact detected_language received from API
   - Log the mapped language value
   - Log the session state update
   
3. Test with actual Hindi/Gujarati audio to see what Whisper returns
   
4. Verify audio encoding is correct (should be WAV, mono, 16000 Hz)
""")

print("\n" + "=" * 80)
