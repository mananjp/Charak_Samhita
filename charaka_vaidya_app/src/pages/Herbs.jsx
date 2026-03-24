import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { motion, AnimatePresence } from 'framer-motion';
import { fetchAllHerbDetails, setFilter, setSelected, clearSelected } from '../features/herbs/herbsSlice';
import { Search, X, BookOpen, FlaskConical, Leaf, AlertTriangle, Heart, ChevronDown, ChevronUp } from 'lucide-react';
import styles from './Herbs.module.css';

// SDG 3 targets that Ayurveda addresses
const SDG3_TARGETS = [
  { icon: '🧬', code: '3.4', title: 'NCDs & Mental Health', herb_tag: 'Adaptogen, Stress' },
  { icon: '🦠', code: '3.3', title: 'Infectious Diseases', herb_tag: 'Antimicrobial, Immunity' },
  { icon: '🧓', code: '3.8', title: 'Universal Health Coverage', herb_tag: 'Accessible, Traditional' },
  { icon: '💊', code: '3.d', title: 'Health Risk Reduction', herb_tag: 'Preventive, Rasayana' },
];

// Herb emoji map for visual richness
const HERB_VISUALS = {
  ashwagandha: { emoji: '⚡', color: '#D4A054', gradient: 'from-amber-50 to-orange-50' },
  brahmi:      { emoji: '🧠', color: '#6B8F6E', gradient: 'from-green-50 to-teal-50' },
  triphala:    { emoji: '🍊', color: '#C05C44', gradient: 'from-orange-50 to-red-50' },
  tulsi:       { emoji: '🌿', color: '#2d9d5c', gradient: 'from-green-50 to-emerald-50' },
  neem:        { emoji: '🌳', color: '#3c7a24', gradient: 'from-lime-50 to-green-50' },
  shatavari:   { emoji: '🌸', color: '#b56fa5', gradient: 'from-pink-50 to-purple-50' },
  default:     { emoji: '🌱', color: '#6B8F6E', gradient: 'from-green-50 to-teal-50' },
};

const HERB_SDG_MAP = {
  'Brahmi': '3.4 — Mental Health & Well-Being',
  'Shankhapushpi': '3.4 — Mental Health & Cognitive Support',
  'Ashwagandha': '3.4 — NCDs & Stress Reduction',
  'Tulsi': '3.3 — Immunity & Infectious Diseases',
  'Neem': '3.3 — Antimicrobial & Skin Health',
  'Giloy': '3.3 — Fever Management & Immunity',
  'Shatavari': '3.7 — Maternal & Reproductive Health',
  'Amla': '3.d — Preventive Health & Immunity',
  'Triphala': '3.4 — Digestive NCDs & Gut Health',
  'Turmeric': '3.4 — Anti-inflammatory & NCD Prevention',
  'Haritaki': '3.4 — Digestive Health',
  'Bibhitaki': '3.3 — Respiratory Health',
  'Ginger': '3.d — Daily Preventive Health',
  'Cumin': '3.d — Digestive & Metabolic Health',
  'Licorice': '3.4 — Ulcers & Respiratory NCDs',
  'Vidari': '3.d — Rejuvenation & Preventive Health',
  'Punarnava': '3.4 — Renal & Liver Health (NCDs)'
};

function getHerbVisual(name = '') {
  return HERB_VISUALS[name.toLowerCase()] || HERB_VISUALS.default;
}

// Property Row
function PropRow({ label, value, icon }) {
  if (!value) return null;
  return (
    <div className={styles.propRow}>
      <span className={styles.propLabel}>{icon} {label}</span>
      <span className={styles.propValue}>{value}</span>
    </div>
  );
}

// Expandable section
function Section({ title, icon, children, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className={styles.section}>
      <button className={styles.sectionHead} onClick={() => setOpen((o) => !o)}>
        <span>{icon} {title}</span>
        {open ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className={styles.sectionBody}
          >
            {children}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// Full Herb Card (expanded view)
function HerbCard({ herb, isExpanded, onToggle }) {
  const key = (herb.name || '').toLowerCase();
  const visual = getHerbVisual(key);

  return (
    <motion.div
      className={`${styles.card} ${isExpanded ? styles.cardExpanded : ''}`}
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.35 }}
    >
      {/* Card Header */}
      <button className={styles.cardHeader} onClick={onToggle}>
        <div className={styles.cardIconWrap} style={{ background: `${visual.color}18`, border: `2px solid ${visual.color}30` }}>
          <span className={styles.cardEmoji}>{visual.emoji}</span>
        </div>
        <div className={styles.cardTitles}>
          <h3 className={styles.cardName}>{herb.name}</h3>
          {herb.english && <p className={styles.cardEnglish}>{herb.english}</p>}
          <div className={styles.cardMeta}>
            {herb.sanskrit && <span className={styles.metaSanskrit}>🕉 {herb.sanskrit}</span>}
            {herb.hindi && <span className={styles.metaHindi}>• {herb.hindi}</span>}
          </div>
        </div>
        <div className={styles.cardChevron}>
          {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </div>
      </button>

      {/* Quick tags always visible */}
      <div className={styles.cardTags}>
        {herb.virya && <span className="chip chip-terra">🔥 {herb.virya}</span>}
        {herb.vipaka && <span className="chip chip-gold">🔄 {herb.vipaka}</span>}
        {herb.rasa && <span className="chip chip-green">👅 {herb.rasa}</span>}
      </div>

      {/* Expandable full details */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            className={styles.cardDetails}
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.4, ease: [0.4, 0, 0.2, 1] }}
          >
            {/* Classical Properties */}
            <div className={styles.classicalProps}>
              <h4 className={styles.detailSubtitle}>⚗️ Classical Properties</h4>
              <div className={styles.propsGrid}>
                <PropRow label="Rasa (Taste)" value={herb.rasa} icon="👅" />
                <PropRow label="Guna (Quality)" value={herb.guna} icon="✨" />
                <PropRow label="Virya (Potency)" value={herb.virya} icon="🔥" />
                <PropRow label="Vipaka" value={herb.vipaka} icon="🔄" />
                <PropRow label="Reference" value={herb.reference} icon="📚" />
              </div>
            </div>

            <Section title="Traditional Uses" icon="📜" defaultOpen>
              <p className={styles.sectionText}>{herb.traditional_uses}</p>
            </Section>

            <Section title="Modern Research" icon="🔬" defaultOpen>
              <p className={styles.sectionText}>{herb.modern_research}</p>
            </Section>

            <Section title="How to Use" icon="💊">
              <p className={styles.sectionText}>{herb.how_to_use}</p>
            </Section>

            {herb.contraindications && (
              <div className={styles.contraindication}>
                <AlertTriangle size={15} />
                <div>
                  <strong>Contraindications:</strong> {herb.contraindications}
                </div>
              </div>
            )}

            {/* SDG 3 tag */}
            <div className={styles.sdgTag}>
              <img
                src="/sdg3_logo.png"
                alt="SDG 3"
                className={styles.sdgTagIcon}
              />
              <span>🎯 Aligns with <strong>SDG {HERB_SDG_MAP[herb.name] || '3.8 — Universal Health Coverage'}</strong></span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default function Herbs() {
  const dispatch = useDispatch();
  const { list, filter, loading, error } = useSelector((s) => s.herbs);
  const [expandedId, setExpandedId] = useState(null);
  const [activeTab, setActiveTab] = useState('glossary'); // 'glossary' | 'sdg'

  useEffect(() => { dispatch(fetchAllHerbDetails()); }, [dispatch]);

  const filtered = list.filter((h) => {
    const q = filter.toLowerCase();
    return (
      (h.name || '').toLowerCase().includes(q) ||
      (h.english || '').toLowerCase().includes(q) ||
      (h.traditional_uses || '').toLowerCase().includes(q) ||
      (h.rasa || '').toLowerCase().includes(q)
    );
  });

  const toggleExpand = (id) => setExpandedId((cur) => cur === id ? null : id);

  return (
    <motion.div
      className={styles.page}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.4 }}
    >
      {/* ── Header ── */}
      <div className={styles.header}>
        <div className={styles.headerLeft}>
          <div className={styles.sdgBadge}>
            <img
              src="/sdg3_logo.png"
              alt="SDG 3"
              className={styles.sdgBadgeIcon}
            />
            <span>SDG 3 · Good Health & Well-Being</span>
          </div>
          <h1 className={styles.title}><Leaf size={28} /> Ayurvedic Herb Glossary</h1>
          <p className={styles.subtitle}>
            Complete monographs from the Charaka Samhita — classical properties, modern research, and dosage guidance.
          </p>
        </div>
      </div>

      {/* ── Tabs ── */}
      <div className={styles.tabs}>
        <button className={`${styles.tab} ${activeTab === 'glossary' ? styles.tabActive : ''}`} onClick={() => setActiveTab('glossary')}>
          <BookOpen size={15} /> Herb Glossary ({list.length} herbs)
        </button>
        <button className={`${styles.tab} ${activeTab === 'sdg' ? styles.tabActive : ''}`} onClick={() => setActiveTab('sdg')}>
          <Heart size={15} /> SDG 3 Integration
        </button>
      </div>

      {/* ── SDG 3 Tab ── */}
      <AnimatePresence mode="wait">
        {activeTab === 'sdg' && (
          <motion.div
            className={styles.sdgPanel}
            key="sdg"
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            {/* Hero banner */}
            <div className={styles.sdgHero}>
              <img
                src="/sdg3_logo.png"
                alt="SDG 3"
                className={styles.sdgHeroIcon}
              />
              <div>
                <h2 className={styles.sdgHeroTitle}>SDG 3 — Good Health & Well-Being</h2>
                <p className={styles.sdgHeroText}>
                  The United Nations' Sustainable Development Goal 3 aims to ensure healthy lives and promote well-being for all ages.
                  Charaka Vaidya bridges ancient Ayurvedic wisdom with this global health agenda — bringing evidence-informed, accessible,
                  and preventive healthcare to everyone.
                </p>
              </div>
            </div>

            {/* SDG 3 Targets */}
            <h3 className={styles.sdgSectionTitle}>SDG 3 Targets Addressed by Ayurveda</h3>
            <div className={styles.sdgTargetGrid}>
              {SDG3_TARGETS.map((t) => (
                <div key={t.code} className={styles.sdgTargetCard}>
                  <span className={styles.sdgTargetIcon}>{t.icon}</span>
                  <div>
                    <div className={styles.sdgTargetCode}>Target {t.code}</div>
                    <div className={styles.sdgTargetTitle}>{t.title}</div>
                    <div className={styles.sdgTargetTag}>{t.herb_tag}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Herb — SDG 3 mapping */}
            <h3 className={styles.sdgSectionTitle}>How Each Herb Supports SDG 3</h3>
            {list.length === 0 && <div className="spinner" />}
            <div className={styles.sdgHerbGrid}>
              {list.map((herb) => {
                const visual = getHerbVisual((herb.name || '').toLowerCase());
                return (
                  <div key={herb.name} className={styles.sdgHerbCard}>
                    <div className={styles.sdgHerbHeader}>
                      <span style={{ fontSize: '1.75rem' }}>{visual.emoji}</span>
                      <div>
                        <strong>{herb.name}</strong>
                        <p className={styles.sdgHerbEnglish}>{herb.english}</p>
                      </div>
                    </div>
                    {herb.modern_research && (
                      <div className={styles.sdgResearchBox}>
                        <FlaskConical size={13} />
                        <p>{herb.modern_research}</p>
                      </div>
                    )}
                    <div className={styles.sdgGoalBadge}>
                      <span>🎯</span> Aligns with SDG {HERB_SDG_MAP[herb.name] || '3.8 — Universal Health Coverage'}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Call to action */}
            <div className={styles.sdgCTA}>
              <div className={styles.sdgCTAText}>
                <h3>🌍 Ayurveda as a Global Health Resource</h3>
                <p>
                  Traditional herbal systems like Ayurveda are recognized by the WHO as integral to achieving universal health coverage —
                  especially in low-resource settings. Charaka Vaidya digitizes this wisdom to make it accessible at scale.
                </p>
              </div>
              <div className={styles.sdgCTAStats}>
                {[
                  { value: '80%', label: 'of world population uses traditional medicine (WHO)' },
                  { value: '3.5B', label: 'people lack access to essential medicines' },
                  { value: '5,000+', label: 'years of documented Ayurvedic practice' },
                ].map(({ value, label }) => (
                  <div key={value} className={styles.sdgStat}>
                    <span className={styles.sdgStatVal}>{value}</span>
                    <span className={styles.sdgStatLabel}>{label}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        {/* ── Glossary Tab ── */}
        {activeTab === 'glossary' && (
          <motion.div key="glossary" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            {/* Search */}
            <div className={styles.searchRow}>
              <div className={styles.searchWrap}>
                <Search size={16} className={styles.searchIcon} />
                <input
                  className={styles.search}
                  placeholder="Search by name, taste, use..."
                  value={filter}
                  onChange={(e) => dispatch(setFilter(e.target.value))}
                />
                {filter && (
                  <button className={styles.clearSearch} onClick={() => dispatch(setFilter(''))}>
                    <X size={14} />
                  </button>
                )}
              </div>
              <span className={styles.herbCount}>
                {filtered.length} herb{filtered.length !== 1 ? 's' : ''}
              </span>
            </div>

            {/* Loading skeletons */}
            {loading && (
              <div className={styles.skeletonList}>
                {[...Array(3)].map((_, i) => (
                  <div key={i} className={styles.skeletonCard}>
                    <div className={styles.skeletonRow}>
                      <div className={styles.skeletonCircle} />
                      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <div className={styles.skeletonLine} style={{ width: '40%' }} />
                        <div className={styles.skeletonLine} style={{ width: '60%' }} />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {error && (
              <div className={styles.error}>
                ❌ {error} — Make sure the backend is running at localhost:8000
              </div>
            )}

            {/* Herb cards */}
            <motion.div className={styles.herbList} layout>
              <AnimatePresence>
                {filtered.map((herb, i) => (
                  <HerbCard
                    key={herb.name || i}
                    herb={herb}
                    isExpanded={expandedId === (herb.name || i)}
                    onToggle={() => toggleExpand(herb.name || i)}
                  />
                ))}
              </AnimatePresence>
              {!loading && filtered.length === 0 && (
                <div className={styles.noResults}>
                  <span>🌱</span>
                  <p>No herbs found. Try searching "bitter" or "pitta".</p>
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
