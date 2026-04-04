import { useDispatch, useSelector } from 'react-redux';
import { motion, AnimatePresence } from 'framer-motion';
import { setAnswer, nextStep, prevStep, resetQuiz, assessDosha } from '../features/dosha/doshaSlice';
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer } from 'recharts';
import { Brain, ChevronRight, ChevronLeft, RefreshCcw, MessageCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import styles from './DoshaQuiz.module.css';

const QUIZ_QUESTIONS = [
  { id: 1, question: 'My body frame is:', options: { vata: 'Thin, light, hard to gain weight', pitta: 'Medium, muscular, moderate build', kapha: 'Large, solid, tendency to gain weight' }},
  { id: 2, question: 'My skin is typically:', options: { vata: 'Dry, rough, or chapped', pitta: 'Warm, reddish, prone to rashes', kapha: 'Smooth, oily, thick and cool' }},
  { id: 3, question: 'My digestion is:', options: { vata: 'Irregular — sometimes great, sometimes poor', pitta: 'Strong — irritable when I skip meals', kapha: 'Slow but steady — rarely starving' }},
  { id: 4, question: 'Under stress, I tend to:', options: { vata: 'Become anxious or worried', pitta: 'Become irritable or angry', kapha: 'Withdraw and become quiet' }},
  { id: 5, question: 'My sleep pattern is:', options: { vata: 'Light, interrupted', pitta: 'Moderate — wake up if too hot', kapha: 'Deep and long — hard to wake up' }},
  { id: 6, question: 'My memory and learning:', options: { vata: 'Quick to learn, quick to forget', pitta: 'Sharp, analytical, great retention', kapha: 'Slow to learn, but never forgets' }},
  { id: 7, question: 'My energy through the day:', options: { vata: 'Variable bursts of energy', pitta: 'Consistent and focused', kapha: 'Steady but slow to start' }},
  { id: 8, question: 'My natural temperament:', options: { vata: 'Creative, enthusiastic, changeable', pitta: 'Ambitious, organized, determined', kapha: 'Calm, patient, nurturing' }},
];

const DOSHA_INFO = {
  vata:  { emoji: '🌬️', color: '#6B8F6E', label: 'Vata',  element: 'Air & Ether' },
  pitta: { emoji: '🔥', color: '#C05C44', label: 'Pitta', element: 'Fire & Water' },
  kapha: { emoji: '🌊', color: '#4a7fa5', label: 'Kapha', element: 'Earth & Water' },
};

export default function DoshaQuiz() {
  const dispatch = useDispatch();
  const { answers, currentStep, result, loading, error } = useSelector((s) => s.dosha);
  const q = QUIZ_QUESTIONS[currentStep];
  const totalSteps = QUIZ_QUESTIONS.length;
  const progress = (currentStep / totalSteps) * 100;

  const handleAnswer = (dosha) => {
    dispatch(setAnswer({ questionId: q.id, answer: dosha }));
  };

  const handleNext = () => {
    if (currentStep < totalSteps - 1) dispatch(nextStep());
    else {
      const formatted = Object.entries(answers).map(([questionId, answer]) => ({
        question_id: parseInt(questionId), answer,
      }));
      dispatch(assessDosha(formatted));
    }
  };

  const handlePrev = () => dispatch(prevStep());
  const handleReset = () => dispatch(resetQuiz());

  // Results view
  if (result) {
    const radarData = Object.entries(result.scores || {}).map(([dosha, score]) => ({
      subject: DOSHA_INFO[dosha]?.label || dosha,
      score: Math.round((score / Object.values(result.scores).reduce((a, b) => a + b, 0)) * 100),
    }));

    return (
      <motion.div className={styles.page} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
        <div className={styles.resultCard}>
          <motion.div className={styles.resultHeader} initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ type: 'spring', stiffness: 300 }}>
            <div className={styles.resultEmoji}>{DOSHA_INFO[result.primary_dosha]?.emoji || '🧘'}</div>
            <h2 className={styles.resultTitle}>Your Prakriti</h2>
            <div className={styles.resultBadge}>
              <span>{DOSHA_INFO[result.primary_dosha]?.label || result.primary_dosha}</span>
              {result.secondary_dosha && <span>-{DOSHA_INFO[result.secondary_dosha]?.label || result.secondary_dosha}</span>}
            </div>
          </motion.div>

          {radarData.length > 0 && (
            <div className={styles.chartWrap}>
              <ResponsiveContainer width="100%" height={250}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="rgba(212,160,84,0.2)" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--clr-muted)', fontSize: 13 }} />
                  <Radar name="Dosha" dataKey="score" fill="rgba(192,92,68,0.15)" stroke="var(--clr-terra)" strokeWidth={2} dot />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          )}

          <div className={styles.doshaScores}>
            {Object.entries(result.scores || {}).map(([dosha, score]) => {
              const total = Object.values(result.scores).reduce((a, b) => a + b, 0);
              const pct = Math.round((score / total) * 100);
              const info = DOSHA_INFO[dosha];
              return (
                <div key={dosha} className={styles.scoreItem}>
                  <span>{info?.emoji} {info?.label}</span>
                  <div className={styles.scoreBar}>
                    <motion.div
                      className={styles.scoreBarFill}
                      style={{ background: info?.color }}
                      initial={{ width: 0 }}
                      animate={{ width: `${pct}%` }}
                      transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
                    />
                  </div>
                  <span className={styles.scorePct}>{pct}%</span>
                </div>
              );
            })}
          </div>

          {result.description && <p className={styles.resultDesc}>{result.description}</p>}

          {result.recommendations?.length > 0 && (
            <div className={styles.recs}>
              <h4>Recommendations</h4>
              <ul>
                {result.recommendations.map((r, i) => <li key={i}>{r}</li>)}
              </ul>
            </div>
          )}

          <div className={styles.resultActions}>
            <Link to="/chat" className="btn btn-primary"><MessageCircle size={16} /> Consult Vaidya</Link>
            <button className="btn btn-outline" onClick={handleReset}><RefreshCcw size={15} /> Retake Quiz</button>
          </div>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div className={styles.page} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4 }}>
      <div className={styles.header}>
        <h1 className={styles.title}><Brain size={26} /> Prakriti Assessment</h1>
        <p className={styles.subtitle}>Discover your Ayurvedic body constitution in 8 questions</p>
      </div>

      <div className={styles.quizCard}>
        {/* Progress */}
        <div className={styles.progressWrap}>
          <div className={styles.progressBar}>
            <motion.div className={styles.progressFill} animate={{ width: `${progress}%` }} transition={{ duration: 0.4 }} />
          </div>
          <span className={styles.progressText}>{currentStep + 1} of {totalSteps}</span>
        </div>

        {/* Question */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 40 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -40 }}
            transition={{ duration: 0.35 }}
          >
            <h2 className={styles.question}>{q.question}</h2>
            <div className={styles.options}>
              {Object.entries(q.options).map(([dosha, label]) => {
                const info = DOSHA_INFO[dosha];
                const isSelected = answers[q.id] === dosha;
                return (
                  <button
                    key={dosha}
                    className={`${styles.optionBtn} ${isSelected ? styles.optionSelected : ''}`}
                    onClick={() => handleAnswer(dosha)}
                    style={isSelected ? { borderColor: info.color, background: `${info.color}12` } : {}}
                  >
                    <span className={styles.optionEmoji}>{info.emoji}</span>
                    <span className={styles.optionLabel}>{label}</span>
                    {isSelected && <span className={styles.optionCheck}>✓</span>}
                  </button>
                );
              })}
            </div>
          </motion.div>
        </AnimatePresence>

        {/* Navigation */}
        <div className={styles.navBtns}>
          {currentStep > 0 && (
            <button className="btn btn-outline" onClick={handlePrev}><ChevronLeft size={16} /> Previous</button>
          )}
          <button
            className="btn btn-primary"
            style={{ marginLeft: 'auto' }}
            onClick={handleNext}
            disabled={!answers[q.id] || loading}
          >
            {loading ? 'Analysing...' : currentStep === totalSteps - 1 ? 'Reveal My Prakriti' : 'Next'}
            {!loading && <ChevronRight size={16} />}
          </button>
        </div>
        {error && <p className={styles.error}>{error}</p>}
      </div>
    </motion.div>
  );
}
