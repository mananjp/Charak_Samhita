import { useState, useCallback, useRef, useEffect } from 'react';
import { Volume2, VolumeX } from 'lucide-react';
import styles from './SpeakButton.module.css';

// BCP47 codes for TTS — support all 3 languages
const LANG_MAP = {
  English: 'en-IN',
  Hindi: 'hi-IN',
  Gujarati: 'gu-IN',
  en: 'en-IN',
  hi: 'hi-IN',
  gu: 'gu-IN',
};

export default function SpeakButton({ text, lang = 'English', size = 'sm', autoPlay = false }) {
  const [speaking, setSpeaking] = useState(false);
  // Load voices immediately and on change
  useEffect(() => {
    const load = () => window.speechSynthesis.getVoices();
    load();
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
      window.speechSynthesis.onvoiceschanged = load;
    }
  }, []);

  const toggle = useCallback(() => {
    if (!window.speechSynthesis) return;

    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
      // If we were the one speaking, just stop.
      if (speaking) return;
    }

    // Strip markdown for clean speech
    const cleanText = text
      .replace(/⚠️|🌿|✨/g, '')
      .replace(/#{1,6}\s?/g, '')
      .replace(/\*{1,2}(.*?)\*{1,2}/g, '$1')
      .replace(/[_~`>]/g, '')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .replace(/^[\s\-\*\d\.]+/gm, '')
      .replace(/\s+/g, ' ')
      .trim()
      .substring(0, 3000);

    if (!cleanText) return;

    const u = new SpeechSynthesisUtterance(cleanText);
    u.lang = LANG_MAP[lang] || 'en-IN';
    u.rate = 1.0; // Standard speed for better clarity in non-English

    const voices = window.speechSynthesis.getVoices();
    const targetCode = u.lang.toLowerCase();
    const langName = lang.toLowerCase();

    // 1. Try exact lang match (e.g. hi-IN)
    // 2. Try start match (e.g. hi)
    // 3. Try name match (e.g. "Hindi")
    const match = voices.find(v => v.lang.toLowerCase() === targetCode) ||
                  voices.find(v => v.lang.toLowerCase().startsWith(targetCode.split('-')[0])) ||
                  voices.find(v => v.name.toLowerCase().includes(langName));

    if (match) u.voice = match;

    u.onstart = () => setSpeaking(true);
    u.onend = () => setSpeaking(false);
    u.onerror = () => setSpeaking(false);

    window.speechSynthesis.speak(u);
  }, [text, lang, speaking]); // Keep speaking here to know if WE were the ones talking

  if (!text) return null;

  return (
    <button
      className={`${styles.speakBtn} ${size === 'lg' ? styles.lg : ''} ${speaking ? styles.active : ''}`}
      onClick={toggle}
      title={speaking ? 'Stop speaking' : `Read aloud (${LANG_MAP[lang] || lang})`}
    >
      {speaking ? <VolumeX size={size === 'lg' ? 16 : 14} /> : <Volume2 size={size === 'lg' ? 16 : 14} />}
      <span>{speaking ? 'Stop' : '🔊 Listen'}</span>
    </button>
  );
}
