import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Heart, Plus, TrendingUp, Calendar, Smile, Frown, Meh, BarChart3 } from 'lucide-react';
import styles from './Wellbeing.module.css';

const MOOD_LABELS = ['', 'Very Poor', 'Poor', 'Okay', 'Good', 'Great'];
const MOOD_EMOJIS = ['', '😞', '😕', '😐', '🙂', '😊'];
const MOOD_COLORS = ['', 'var(--clr-terra)', '#ed8936', 'var(--clr-gold)', 'var(--clr-sage)', 'var(--clr-forest)'];

function getToday() { return new Date().toISOString().split('T')[0]; }

export default function Wellbeing() {
  const [log, setLog] = useState(() => {
    try { return JSON.parse(localStorage.getItem('wellbeing_log') || '[]'); }
    catch { return []; }
  });
  const [mood, setMood] = useState(3);
  const [medicated, setMedicated] = useState('No');
  const [symptoms, setSymptoms] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const todayExists = log.some((e) => e.date === getToday());
  const last7 = log.filter((e) => {
    const d = new Date(e.date);
    const now = new Date();
    return (now - d) / 86400000 <= 7;
  });

  const save = () => {
    const entry = { date: getToday(), mood, medicated, symptoms };
    const newLog = [...log, entry];
    setLog(newLog);
    localStorage.setItem('wellbeing_log', JSON.stringify(newLog));
    setSubmitted(true);
    setSymptoms('');
    setMood(3);
  };

  // Avg mood
  const avgMood = last7.length > 0
    ? (last7.reduce((sum, e) => sum + e.mood, 0) / last7.length).toFixed(1)
    : null;

  return (
    <motion.div
      className={styles.page}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div className={styles.header}>
        <div className={styles.headerIcon}>
           <Heart size={32} color="var(--clr-forest)" />
        </div>
        <h1 className={styles.title}>Well-Being Tracker</h1>
        <p className={styles.subtitle}>Daily Ayurvedic self-assessment — track your health and alignment with SDG 3</p>
      </div>

      {/* SDG 3 badge */}
      <div className={styles.sdgBadge}>
        <img
          src="/sdg3_logo.png"
          alt="SDG 3"
          className={styles.sdgIcon}
        />
        <span>Aligned with <strong>SDG 3</strong> — Good Health & Well-Being · Personal health monitoring</span>
      </div>

      {/* Check-in form */}
      {!todayExists && !submitted ? (
        <motion.div
          className={styles.formCard}
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h2 className={styles.formTitle}><Calendar size={18} /> Today's Check-In</h2>

          <div className={styles.field}>
            <label className={styles.fieldLabel}>How are you feeling today?</label>
            <div className={styles.moodSlider}>
              {[1, 2, 3, 4, 5].map((v) => (
                <button
                  key={v}
                  className={`${styles.moodBtn} ${mood === v ? styles.moodActive : ''}`}
                  style={mood === v ? { borderColor: MOOD_COLORS[v], background: `${MOOD_COLORS[v]}15` } : {}}
                  onClick={() => setMood(v)}
                >
                  <span className={styles.moodEmoji}>{MOOD_EMOJIS[v]}</span>
                  <span className={styles.moodLabel}>{MOOD_LABELS[v]}</span>
                </button>
              ))}
            </div>
          </div>

          <div className={styles.field}>
            <label className={styles.fieldLabel}>Did you take any Ayurvedic herbs/medicine today?</label>
            <div className={styles.radioGroup}>
              {['Yes', 'No'].map((opt) => (
                <button
                  key={opt}
                  className={`${styles.radioBtn} ${medicated === opt ? styles.radioActive : ''}`}
                  onClick={() => setMedicated(opt)}
                >
                  {opt}
                </button>
              ))}
            </div>
          </div>

          <div className={styles.field}>
            <label className={styles.fieldLabel}>Any symptoms or notes?</label>
            <input
              className={styles.textInput}
              placeholder="e.g. mild headache, fatigue, good digestion..."
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
            />
          </div>

          <button className={styles.submitBtn} onClick={save}>
            <Plus size={16} /> Save Today's Entry
          </button>
        </motion.div>
      ) : (
        <div className={styles.checkedIn}>
          <Smile size={28} />
          <p>✅ You've already checked in today! Come back tomorrow.</p>
        </div>
      )}

      {/* Weekly trend */}
      {last7.length > 0 && (
        <div className={styles.trendSection}>
          <h3 className={styles.sectionTitle}><TrendingUp size={18} /> 7-Day Mood Trend</h3>

          <div className={styles.statsRow}>
            <div className={styles.statCard}>
              <BarChart3 size={20} />
              <div>
                <div className={styles.statVal}>{avgMood}</div>
                <div className={styles.statLabel}>Avg Mood</div>
              </div>
            </div>
            <div className={styles.statCard}>
              <Calendar size={20} />
              <div>
                <div className={styles.statVal}>{last7.length}</div>
                <div className={styles.statLabel}>Check-ins</div>
              </div>
            </div>
            <div className={styles.statCard}>
              <Heart size={20} />
              <div>
                <div className={styles.statVal}>{last7.filter(e => e.medicated === 'Yes').length}</div>
                <div className={styles.statLabel}>Herbal Days</div>
              </div>
            </div>
          </div>

          {/* Visual bar chart */}
          <div className={styles.chartBars}>
            {last7.map((entry, i) => (
              <div key={i} className={styles.chartBar}>
                <div
                  className={styles.barFill}
                  style={{ height: `${entry.mood * 20}%`, background: MOOD_COLORS[entry.mood] }}
                >
                  {MOOD_EMOJIS[entry.mood]}
                </div>
                <span className={styles.barDate}>{entry.date.slice(5)}</span>
              </div>
            ))}
          </div>

          {/* Log table */}
          <div className={styles.logTable}>
            <div className={styles.logHeader}>
              <span>Date</span><span>Mood</span><span>Herbal</span><span>Notes</span>
            </div>
            {[...last7].reverse().map((e, i) => (
              <div key={i} className={styles.logRow}>
                <span>{e.date}</span>
                <span>{MOOD_EMOJIS[e.mood]} {MOOD_LABELS[e.mood]}</span>
                <span>{e.medicated}</span>
                <span className={styles.logNotes}>{e.symptoms || '—'}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className={styles.privacy}>
        🔒 All data is stored only in your browser (localStorage) and is never sent to any server.
      </div>
    </motion.div>
  );
}
