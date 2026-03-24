import { useState, useRef, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { sendMessage, addUserMessage, clearChat, toggleSimpleMode } from '../features/chat/chatSlice';
import VoiceInput from '../components/Voice/VoiceInput';
import SpeakButton from '../components/Voice/SpeakButton';
import { MessageCircle, Send, Trash2, Sparkles, BookOpen, Globe, AlertTriangle } from 'lucide-react';
import styles from './Chat.module.css';

const LANGUAGES = [
  { code: 'English',  label: 'English',  flag: '🇬🇧', short: 'EN' },
  { code: 'Hindi',    label: 'हिन्दी',   flag: '🇮🇳', short: 'HI' },
  { code: 'Gujarati', label: 'ગુજરાતી', flag: '🇮🇳', short: 'GU' },
];

const LANG_TTS_MAP = { English: 'en', Hindi: 'hi', Gujarati: 'gu' };

const SUGGESTIONS = {
  English: [
    'I have constant bloating after meals',
    'Tell me about Ashwagandha benefits',
    'How to structure my daily routine?',
    'What foods should I avoid in summer?',
    'Explain Triphala and how to use it',
  ],
  Hindi: [
    'मुझे खाने के बाद पेट फूलने की समस्या है',
    'अश्वगंधा के फायदे बताएं',
    'दैनिक दिनचर्या कैसे बनाएं?',
    'गर्मी में कौन से खाद्य पदार्थ से बचें?',
  ],
  Gujarati: [
    'ખોરાક પછી પેટ ફૂલવાની સમસ્યા છે',
    'અશ્વગંધાના ફાયદા બતાવો',
    'દૈનિક દિનચર્યા કેવી રીતે બનાવી?',
    'ઉનાળામાં કયા ખોરાક ટાળવા?',
  ],
};

export default function Chat() {
  const dispatch = useDispatch();
  const { messages, sources, loading, simpleMode, error } = useSelector((s) => s.chat);
  const [input, setInput] = useState('');
  const [selectedLang, setSelectedLang] = useState('English');
  const [langOpen, setLangOpen] = useState(false);
  const endRef = useRef(null);
  const langRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e) => {
      if (langRef.current && !langRef.current.contains(e.target)) setLangOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleSend = (text) => {
    const query = (text || input).trim();
    if (!query) return;
    dispatch(addUserMessage(query));
    dispatch(sendMessage({
      query,
      history: messages,
      simple_mode: simpleMode,
      language: selectedLang,
    }));
    setInput('');
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  const handleVoice = (text, langCode) => {
    // When voice transcribes, use the text but keep the manually selected language
    setInput(text);
    setTimeout(() => handleSend(text), 200);
  };

  const currentLang = LANGUAGES.find((l) => l.code === selectedLang);
  const suggestions = SUGGESTIONS[selectedLang] || SUGGESTIONS.English;

  return (
    <motion.div
      className={styles.page}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div className={styles.header}>
        <div>
          <h1 className={styles.title}><MessageCircle size={26} /> Consult Vaidya</h1>
          <p className={styles.subtitle}>Ask in English, Hindi or Gujarati — responses come in your chosen language</p>
        </div>
        <div className={styles.toolbar}>
          {/* Language picker */}
          <div className={styles.langPicker} ref={langRef}>
            <button className={styles.langToggle} onClick={() => setLangOpen((o) => !o)}>
              <Globe size={14} />
              <span className={styles.langFlag}>{currentLang?.flag}</span>
              <span>{currentLang?.label}</span>
              <span className={styles.langChevron}>▾</span>
            </button>
            <AnimatePresence>
              {langOpen && (
                <motion.div
                  className={styles.langDropdown}
                  initial={{ opacity: 0, y: -8, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -8, scale: 0.95 }}
                  transition={{ duration: 0.15 }}
                >
                  <div className={styles.langDropdownHeader}>
                    <Globe size={12} /> Response Language
                  </div>
                  {LANGUAGES.map((lang) => (
                    <button
                      key={lang.code}
                      className={`${styles.langOption} ${selectedLang === lang.code ? styles.langSelected : ''}`}
                      onClick={() => { setSelectedLang(lang.code); setLangOpen(false); }}
                    >
                      <span className={styles.langOptFlag}>{lang.flag}</span>
                      <span className={styles.langOptLabel}>{lang.label}</span>
                      <span className={styles.langOptShort}>{lang.short}</span>
                      {selectedLang === lang.code && <span className={styles.langCheck}>✓</span>}
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <button
            className={`${styles.modeBtn} ${simpleMode ? styles.modeBtnActive : ''}`}
            onClick={() => dispatch(toggleSimpleMode())}
          >
            <Sparkles size={14} /> Simple
          </button>
          <button className={styles.clearBtn} onClick={() => dispatch(clearChat())}>
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      {/* Chat messages */}
      <div className={styles.chatArea}>
        {messages.length === 0 && (
          <div className={styles.empty}>
            <span className={styles.emptyFlower}>🌿</span>
            <h2 className={styles.emptyTitle}>Namaste!</h2>
            <p>I'm Charaka Vaidya. Select your language above, then ask me anything.</p>

            <div className={styles.currentLangBanner}>
              <Globe size={16} />
              Responding in <strong>{currentLang?.flag} {currentLang?.label}</strong>
            </div>

            <div className={styles.chips}>
              {suggestions.map((s) => (
                <button key={s} className={styles.chip} onClick={() => handleSend(s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              className={`${styles.bubble} ${msg.role === 'user' ? styles.bubbleUser : styles.bubbleBot}`}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.25 }}
            >
              {msg.role === 'assistant' ? (
                <div className={styles.botContent}>
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              ) : (
                <span>{msg.content}</span>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <div className={styles.typing}>
            <span /><span /><span />
          </div>
        )}
        <div ref={endRef} />
      </div>

      {/* API Error display */}
      {error && (
        <div className={styles.chatError}>
          <AlertTriangle size={16} />
          <span>Error connecting to AI: {error}</span>
        </div>
      )}

      {/* Sources panel */}
      {sources.length > 0 && (
        <div className={styles.srcPanel}>
          <h4><BookOpen size={14} /> Sources from Charaka Samhita</h4>
          {sources.map((s, i) => (
            <div key={i} className={styles.srcCard}>
              <div className={styles.srcMeta}>
                <span className={styles.srcSthana}>{s.sthana}</span>
                <span className={styles.srcAdhyaya}>{s.adhyaya}</span>
                {s.score && <span className={styles.srcScore}>{(s.score * 100).toFixed(0)}%</span>}
              </div>
              <p className={styles.srcPreview}>{s.preview}</p>
              {s.tags?.length > 0 && (
                <div className={styles.srcTags}>
                  {s.tags.map((t) => <span key={t} className={styles.srcTag}>{t}</span>)}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Input area */}
      <div className={styles.inputArea}>
        <VoiceInput onTranscription={handleVoice} lang={LANG_TTS_MAP[selectedLang]} compact />
        <textarea
          className={styles.input}
          placeholder={
            selectedLang === 'Hindi' ? 'अपना सवाल यहाँ लिखें...' :
            selectedLang === 'Gujarati' ? 'તમારો પ્રશ્ન અહીં લખો...' :
            'Ask about symptoms, herbs, doshas...'
          }
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
          rows={1}
        />
        <button
          className={styles.sendBtn}
          onClick={() => handleSend()}
          disabled={!input.trim() || loading}
        >
          <Send size={18} />
        </button>
      </div>

      <p className={styles.disclaimer}>
        ⚠️ Educational only. Always consult a qualified practitioner for health decisions.
      </p>
    </motion.div>
  );
}
