import { NavLink, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useSelector } from 'react-redux';
import { useState } from 'react';
import { MessageCircle, Leaf, Brain, Sun, BookOpen, Heart, Menu, X, Wifi, WifiOff } from 'lucide-react';
import styles from './Navbar.module.css';

const navItems = [
  { to: '/chat',    label: 'Consult Vaidya',  icon: MessageCircle },
  { to: '/herbs',   label: 'Herbs',           icon: Leaf },
  { to: '/dosha',   label: 'Prakriti',        icon: Brain },
  { to: '/routine', label: 'Dinacharya',      icon: Sun },
  { to: '/samhita', label: 'Samhita',         icon: BookOpen },
  { to: '/wellbeing', label: 'Well-Being',    icon: Heart },
];

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);
  const status = useSelector((s) => s.health.status);
  const location = useLocation();

  return (
    <motion.header
      className={styles.header}
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
    >
      <div className={styles.inner}>
        {/* Logo */}
        <NavLink to="/" className={styles.logo}>
          <span className={styles.logoEmoji}>🌿</span>
          <span className={styles.logoText}>
            <span className={styles.logoMain}>Charaka</span>
            <span className={styles.logoSub}>Vaidya</span>
          </span>
        </NavLink>

        {/* Desktop Nav */}
        <nav className={styles.nav}>
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `${styles.navLink} ${isActive ? styles.active : ''}`
              }
            >
              <Icon size={15} />
              {label}
              {location.pathname === to && (
                <motion.span
                  layoutId="navActiveIndicator"
                  className={styles.activeIndicator}
                  transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                />
              )}
            </NavLink>
          ))}
        </nav>

        {/* Status + mobile menu */}
        <div className={styles.right}>
          {/* Health indicator */}
          <span className={styles.statusDot} title={`API: ${status}`}>
            {status === 'online'
              ? <Wifi size={15} color="var(--clr-sage)" />
              : <WifiOff size={15} color="var(--clr-terra)" />
            }
          </span>

          {/* Mobile hamburger */}
          <button
            className={styles.hamburger}
            onClick={() => setMenuOpen((o) => !o)}
            aria-label="Toggle menu"
          >
            {menuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      <AnimatePresence>
        {menuOpen && (
          <motion.div
            className={styles.mobileMenu}
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {navItems.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `${styles.mobileLink} ${isActive ? styles.activeMobile : ''}`
                }
                onClick={() => setMenuOpen(false)}
              >
                <Icon size={18} /> {label}
              </NavLink>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.header>
  );
}
