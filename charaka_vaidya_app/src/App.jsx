import { Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { checkHealth } from './features/health/healthSlice';

import Navbar from './components/Layout/Navbar';
import Home from './pages/Home';
import Chat from './pages/Chat';
import Herbs from './pages/Herbs';
import DoshaQuiz from './pages/DoshaQuiz';
import DailyRoutine from './pages/DailyRoutine';
import SamhitaExplorer from './pages/SamhitaExplorer';
import Wellbeing from './pages/Wellbeing';

function App() {
  const location = useLocation();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(checkHealth());
  }, [dispatch]);

  return (
    <div style={{ minHeight: '100vh', background: 'var(--clr-parchment)' }}>
      <Navbar />
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/herbs" element={<Herbs />} />
          <Route path="/dosha" element={<DoshaQuiz />} />
          <Route path="/routine" element={<DailyRoutine />} />
          <Route path="/samhita" element={<SamhitaExplorer />} />
          <Route path="/wellbeing" element={<Wellbeing />} />
        </Routes>
      </AnimatePresence>
    </div>
  );
}

export default App;
