import { motion } from 'framer-motion';
import { useDispatch } from 'react-redux';
import { setQuery } from '../features/samhita/samhitaSlice';
import { BookOpen, Book, Info, Zap, ArrowRight } from 'lucide-react';
import styles from './SamhitaExplorer.module.css';

const SAMHITA_BOOKS = [
  'Sutrasthana', 'Nidanasthana', 'Vimanasthana', 'Sharirasthana', 
  'Indriyasthana', 'Chikitsasthana', 'Kalpasthana', 'Siddhisthana'
];

const GLOSSARY_TERMS = [
  { term: 'Agni', def: 'Digestive fire / metabolic strength' },
  { term: 'Ama', def: 'Undigested metabolic waste / toxin accumulation' },
  { term: 'Ojas', def: 'Vital essence / immunity force' },
  { term: 'Prana', def: 'Life force / vital energy' },
  { term: 'Rasayana', def: 'Rejuvenation therapy' },
  { term: 'Prakriti', def: 'Individual body constitution' },
  { term: 'Srotas', def: 'Body channels / micro-circulatory systems' },
];

const DOSHA_REF = [
  { term: 'Vata', icon: '🌬️', desc: "Movement and nervous energy principle, like wind" },
  { term: 'Pitta', icon: '🔥', desc: "Transformation and metabolic engine, like fire" },
  { term: 'Kapha', icon: '🌊', desc: "Structure, stability and lubrication, like earth" },
];

export default function SamhitaExplorer() {
  const dispatch = useDispatch();

  return (
    <motion.div 
      className={styles.page} 
      initial={{ opacity: 0 }} 
      animate={{ opacity: 1 }} 
      transition={{ duration: 0.5 }}
    >
      <div className={styles.header}>
        <div className={styles.headerIcon}>
          <BookOpen size={36} color="var(--clr-forest)" />
        </div>
        <h1 className={styles.title}>The Samhita Sanctuary</h1>
        <p className={styles.subtitle}>Navigate 5,000 years of clinical wisdom through the 8 core books and ancient definitions.</p>
      </div>

      <div className={styles.cardGrid}>
        {/* Card 1: Books */}
        <motion.div 
          className={styles.explorerCard}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <div className={styles.cardHeader}>
            <div className={styles.iconWrap}>
              <Book size={24} color="var(--clr-forest)" />
            </div>
            <div>
              <h2 className={styles.cardTitle}>Classical Books</h2>
              <p className={styles.cardSubtitle}>The 8 Essential Sthanas</p>
            </div>
          </div>
          <div className={styles.cardBody}>
            <ul className={styles.bookList}>
              {SAMHITA_BOOKS.map((b) => (
                <li key={b} className={styles.bookItem} onClick={() => dispatch(setQuery(`About ${b}`))}>
                  <span>{b}</span>
                  <ArrowRight size={14} className={styles.arrow} />
                </li>
              ))}
            </ul>
          </div>
        </motion.div>

        {/* Card 2: Glossary */}
        <motion.div 
          className={styles.explorerCard}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className={styles.cardHeader}>
            <div className={styles.iconWrap}>
              <Info size={24} color="var(--clr-forest)" />
            </div>
            <div>
              <h2 className={styles.cardTitle}>Healing Glossary</h2>
              <p className={styles.cardSubtitle}>Key Classical Concepts</p>
            </div>
          </div>
          <div className={styles.cardBody}>
            <div className={styles.glossaryScroll}>
              {GLOSSARY_TERMS.map((g) => (
                <div key={g.term} className={styles.glossaryItem}>
                  <strong className={styles.glossaryTerm}>{g.term}</strong>
                  <p className={styles.glossaryDef}>{g.def}</p>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Card 3: Doshas */}
        <motion.div 
          className={styles.explorerCard}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className={styles.cardHeader}>
            <div className={styles.iconWrap}>
              <Zap size={24} color="var(--clr-forest)" />
            </div>
            <div>
              <h2 className={styles.cardTitle}>Dosha Reference</h2>
              <p className={styles.cardSubtitle}>The Three Vital Pillars</p>
            </div>
          </div>
          <div className={styles.cardBody}>
            <div className={styles.doshaList}>
              {DOSHA_REF.map((d) => (
                <div key={d.term} className={styles.doshaCard}>
                  <div className={styles.doshaIcon}>{d.icon}</div>
                  <div className={styles.doshaLabel}>
                    <strong>{d.term}</strong>
                    <span>{d.desc}</span>
                  </div>
                </div>
              ))}
            </div>
            <div className={styles.cardFooter}>
              <span>Navigate for Verse Depth</span>
              <ArrowRight size={16} />
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
