import { useState, useRef, useCallback } from 'react';
import { Mic, MicOff, Loader2 } from 'lucide-react';
import styles from './VoiceInput.module.css';

export default function VoiceInput({ onTranscription, lang, compact = false }) {
  const [recording, setRecording] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  const [error, setError] = useState(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const startRecording = useCallback(async () => {
    setError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        if (blob.size < 100) {
          setError('Recording too short');
          return;
        }
        await transcribe(blob, lang);
      };

      mediaRecorder.start();
      setRecording(true);
    } catch (err) {
      setError('Microphone access denied');
    }
  }, [lang]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  }, [recording]);

  const transcribe = async (blob, targetLang) => {
    setTranscribing(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', blob, 'recording.webm');

      const url = targetLang ? `http://localhost:8888/transcribe?language=${targetLang}` : 'http://localhost:8888/transcribe';
      const res = await fetch(url, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Server error ${res.status}`);
      }

      const data = await res.json();
      if (data.text && onTranscription) {
        onTranscription(data.text, data.detected_language, data.language_name);
      }
    } catch (err) {
      setError(err.message || 'Transcription failed');
    } finally {
      setTranscribing(false);
    }
  };

  return (
    <button
      className={`${styles.micBtn} ${recording ? styles.micRecording : ''}`}
      onClick={recording ? stopRecording : startRecording}
      disabled={transcribing}
      title={recording ? 'Stop recording' : transcribing ? 'Transcribing...' : 'Voice input (auto-detects Hindi, English, Gujarati)'}
    >
      {transcribing ? <Loader2 size={18} className={styles.spin} /> : recording ? <MicOff size={18} /> : <Mic size={18} />}
    </button>
  );
}
