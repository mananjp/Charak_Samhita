import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { motion, AnimatePresence } from 'framer-motion';
import { fetchRoutine, setSeason } from '../features/routine/routineSlice';
import { Sun, Leaf, AlertTriangle, Utensils } from 'lucide-react';
import styles from './DailyRoutine.module.css';

const SEASONS = [
  { key: 'spring',  label: '🌸 Spring',  sanskrit: 'Vasanta' },
  { key: 'summer',  label: '☀️ Summer',  sanskrit: 'Grishma' },
  { key: 'monsoon', label: '🌧️ Monsoon', sanskrit: 'Varsha' },
  { key: 'autumn',  label: '🍂 Autumn',  sanskrit: 'Sharad' },
  { key: 'winter',  label: '❄️ Winter',  sanskrit: 'Hemanta' },
];

// Icons for dinacharya steps
const STEP_ICONS = ['🌙','💧','🪥','🌊','🧘','🏃','🛁','🍵','☀️','🍽️','🚶','🌙'];

export default function DailyRoutine() {
  const dispatch = useDispatch();
  const { data, season, loading, error } = useSelector((s) => s.routine);
  const [activeSeason, setActiveSeason] = useState('spring');

  useEffect(() => {
    dispatch(setSeason(activeSeason));
    dispatch(fetchRoutine(activeSeason));
  }, [dispatch, activeSeason]);

  // The API returns: { season_key, season, wake, exercise, diet_focus, herbs[], avoid[], dinacharya[] }
  const dinacharya = data?.dinacharya || [];
  const overviewFields = data ? [
    { icon: '⏰', label: 'Wake Up', value: data.wake },
    { icon: '🏋️', label: 'Exercise', value: data.exercise },
    { icon: '🥗', label: 'Diet Focus', value: data.diet_focus },
  ] : [];

  return (
    <motion.div
      className={styles.page}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      {/* Header */}
      <div className={styles.header}>
        <h1 className={styles.title}><Sun size={28} /> Dinacharya</h1>
        <p className={styles.subtitle}>The Ayurvedic 24-hour daily routine for vibrant health — tailored by season</p>
      </div>

      {/* Season tabs */}
      <div className={styles.seasonTabs}>
        {SEASONS.map(({ key, label, sanskrit }) => (
          <button
            key={key}
            className={`${styles.seasonTab} ${activeSeason === key ? styles.seasonActive : ''}`}
            onClick={() => setActiveSeason(key)}
          >
            {label}
            <span className={styles.tabSanskrit}>{sanskrit}</span>
          </button>
        ))}
      </div>

      {loading && <div className="spinner" />}

      {error && (
        <div className={styles.error}>
          Could not load routine from API. Please ensure the backend is running.
        </div>
      )}

      {!loading && data && (
        <>
          {/* Season hero */}
          <motion.div
            className={styles.seasonHero}
            key={activeSeason}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <div className={styles.seasonHeroLeft}>
              <div className={styles.seasonBadge}>{SEASONS.find(s => s.key === activeSeason)?.label}</div>
              <h2 className={styles.seasonName}>{data.season}</h2>
            </div>
            <div className={styles.overviewCards}>
              {overviewFields.map(({ icon, label, value }) => value && (
                <div key={label} className={styles.overviewCard}>
                  <span className={styles.overviewIcon}>{icon}</span>
                  <div>
                    <div className={styles.overviewLabel}>{label}</div>
                    <div className={styles.overviewValue}>{value}</div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Herbs for this season */}
          {data.herbs?.length > 0 && (
            <div className={styles.seasonHerbs}>
              <h3 className={styles.sectionSmallTitle}><Leaf size={16} /> Recommended Herbs</h3>
              <div className={styles.herbChips}>
                {data.herbs.map((h) => (
                  <span key={h} className={styles.herbChip}>{h}</span>
                ))}
              </div>
            </div>
          )}

          {/* Avoid list */}
          {data.avoid?.length > 0 && (
            <div className={styles.avoidBox}>
              <AlertTriangle size={16} />
              <div>
                <strong>Avoid this season:</strong>{' '}
                {data.avoid.join(' • ')}
              </div>
            </div>
          )}

          {/* Dinacharya Timeline */}
          <h3 className={styles.timelineTitle}>Daily Routine Steps</h3>
          <motion.div
            className={styles.timeline}
            key={activeSeason + '-timeline'}
            initial="hidden"
            animate="visible"
            variants={{ visible: { transition: { staggerChildren: 0.07 } } }}
          >
            {dinacharya.map((step, i) => (
              <motion.div
                key={i}
                className={styles.timelineItem}
                variants={{
                  hidden: { opacity: 0, x: -20 },
                  visible: { opacity: 1, x: 0, transition: { duration: 0.4 } },
                }}
              >
                <div className={styles.timelineLeft}>
                  <div className={styles.timelineIcon}>
                    {STEP_ICONS[i] || '🌿'}
                  </div>
                  {i < dinacharya.length - 1 && <div className={styles.timelineLine} />}
                </div>
                <div className={styles.timelineContent}>
                  <div className={styles.stepNumber}>Step {i + 1}</div>
                  <p className={styles.timelineDesc}>{step}</p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </>
      )}
    </motion.div>
  );
}
