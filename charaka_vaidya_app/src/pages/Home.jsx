import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { MessageCircle, Leaf, Brain, Sun, BookOpen, Search, ArrowRight, Sparkles, HeartHandshake } from 'lucide-react';
import styles from './Home.module.css';

const features = [
  {
    to: '/chat',
    icon: MessageCircle,
    title: 'Consult AI Vaidya',
    description: 'Direct AI consultation powered by Charaka Samhita RAG. Ask about symptoms, herbs, and classical treatments.',
    color: '#C05C44',
    bg: 'rgba(192,92,68,0.1)',
  },
  {
    to: '/herbs',
    icon: Leaf,
    title: 'Herb Glossary',
    description: 'Explore 120+ Ayurvedic herbs with botanical properties, clinical uses, and UN SDG 3 health targets.',
    color: '#6B8F6E',
    bg: 'rgba(107,143,110,0.1)',
  },
  {
    to: '/dosha',
    icon: Brain,
    title: 'Prakriti Assessment',
    description: 'Identify your unique constitution (Vata, Pitta, Kapha) through our classical eight-fold assessment quiz.',
    color: '#D4A054',
    bg: 'rgba(212,160,84,0.1)',
  },
  {
    to: '/routine',
    icon: Sun,
    title: 'Seasonal Dinacharya',
    description: 'Dynamic daily routines tailored to the current season (Ritu) for optimal hormonal and metabolic balance.',
    color: '#C05C44',
    bg: 'rgba(192,92,68,0.1)',
  },
  {
    to: '/samhita',
    icon: BookOpen,
    title: 'Samhita Explorer',
    description: 'Navigate the 8 books of the Charaka Samhita. Search thousands of classical verses for hidden healing wisdom.',
    color: '#1E3A34',
    bg: 'rgba(30,58,52,0.1)',
  },
];

const quotes = [
  '"The physician who knows the science of Ayurveda has the power to root out all diseases." — Acharya Charaka',
  '"The body is the primary instrument of dharma and all pursuits of life." — Charaka Samhita',
  '"Health is a state of equilibrium of the three doshas, seven dhatus, and three wastes." — Charaka Samhita',
];

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } },
};

const itemVariants = {
  hidden: { opacity: 0, scale: 0.95, y: 30 },
  visible: { opacity: 1, scale: 1, y: 0, transition: { duration: 0.7, ease: [0.4, 0, 0.2, 1] } },
};

export default function Home() {
  return (
    <main className={styles.main}>
      {/* Dynamic Background Elements */}
      <div className={styles.bgGlow1} />
      <div className={styles.bgGlow2} />
      
      {/* Hero Section */}
      <motion.section
        className={styles.hero}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <motion.div
          className={styles.heroBadge}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.6 }}
        >
          <Sparkles size={14} className={styles.sparkle} />
          Certified Ancient Wisdom · RAG-Powered Intelligence
        </motion.div>

        <motion.h1
          className={styles.heroTitle}
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.9, ease: "easeOut" }}
        >
          Healing the Future with
          <br />
          <span className={styles.heroAccent}>Ancient Enlightenment</span>
        </motion.h1>

        <motion.p
          className={styles.heroSubtitle}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.7 }}
        >
          Charaka Vaidya bridges 5,000 years of Ayurvedic healing with state-of-the-art AI.
          The wisdom of the <em>Charaka Samhita</em>, now optimized for the modern world.
        </motion.p>

        <motion.div
          className={styles.heroCTA}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.6 }}
        >
          <Link to="/chat" className={`${styles.ctaBtn} ${styles.ctaPrimary}`}>
            <MessageCircle size={20} />
            Consult AI Vaidya
          </Link>
          <Link to="/dosha" className={`${styles.ctaBtn} ${styles.ctaOutline}`}>
            Test Your Prakriti
          </Link>
        </motion.div>

        {/* Floating Quote */}
        <motion.div
          className={styles.quoteWrap}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.2, duration: 1 }}
        >
          <span className={styles.quoteMark}>“</span>
          <p className={styles.quoteText}>{quotes[0]}</p>
        </motion.div>
      </motion.section>

      {/* Features Showcase */}
      <section className={styles.featuresSection}>
        <motion.div
          className={styles.sectionHeader}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
        >
          <h2 className={styles.sectionTitle}>The Sanctuary of Knowledge</h2>
          <p className={styles.sectionSubtitle}>
            Precision health features rooted in the world's oldest medical treatises.
          </p>
        </motion.div>

        <motion.div
          className={styles.featureGrid}
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-80px' }}
        >
          {features.map(({ to, icon: Icon, title, description, color, bg }) => (
            <motion.div key={to} variants={itemVariants}>
              <Link to={to} className={styles.featureCard}>
                <div className={styles.featureIconWrap} style={{ background: bg }}>
                  <Icon size={28} color={color} />
                </div>
                <div className={styles.featureBody}>
                  <h3 className={styles.featureTitle}>{title}</h3>
                  <p className={styles.featureDesc}>{description}</p>
                </div>
                <div className={styles.featureFooter}>
                  <span>Enter</span>
                  <ArrowRight size={16} />
                </div>
              </Link>
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* Trust & Impact Banner */}
      <motion.section
        className={styles.impactSection}
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.8 }}
      >
        <div className={styles.sdgBanner}>
          <div className={styles.sdgContent}>
            <div className={styles.sdgBadge}>
              <HeartHandshake size={24} />
              <span>Aligned with UN Sustainable Development</span>
            </div>
            <h3 className={styles.sdgTitle}>SDG 3 — Good Health & Well-Being</h3>
            <p className={styles.sdgDesc}>
              We are committed to democratizing preventive Ayurvedic healthcare. 
              By digitizing classical wisdom, we enable evidence-informed wellness for all.
            </p>
          </div>
          <div className={styles.sdgVisual}>
              <img
                src="/sdg3_logo.png"
                alt="SDG 3"
                className={styles.sdgImage}
              />
          </div>
        </div>
      </motion.section>

      {/* Scientific Foundation Stats */}
      <motion.section
        className={styles.statsSection}
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 1 }}
      >
        <div className={styles.statsGrid}>
          {[
            { value: '5K+', label: 'Years of Tradition' },
            { value: '17', label: 'SDG 3 Targets' },
            { value: '88', label: 'Sthanas & Chapters' },
            { value: '∞', label: 'Potential for Healing' },
          ].map(({ value, label }) => (
            <div key={label} className={styles.statItem}>
              <span className={styles.statValue}>{value}</span>
              <span className={styles.statLabel}>{label}</span>
            </div>
          ))}
        </div>
      </motion.section>
    </main>
  );
}
