import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Opportunities from './pages/Opportunities';
import Assets from './pages/Assets';
import Alerts from './pages/Alerts';
import Settings from './pages/Settings';
import './styles/main.css';

function App() {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-logo">
          📈 Trading Detector
        </div>
        <ul className="sidebar-menu">
          <li>
            <Link
              to="/"
              className={location.pathname === '/' ? 'active' : ''}
              onClick={() => setMobileMenuOpen(false)}
            >
              📊 Dashboard
            </Link>
          </li>
          <li>
            <Link
              to="/opportunities"
              className={location.pathname === '/opportunities' ? 'active' : ''}
              onClick={() => setMobileMenuOpen(false)}
            >
              💎 Oportunidades
            </Link>
          </li>
          <li>
            <Link
              to="/assets"
              className={location.pathname === '/assets' ? 'active' : ''}
              onClick={() => setMobileMenuOpen(false)}
            >
              📋 Activos
            </Link>
          </li>
          <li>
            <Link
              to="/alerts"
              className={location.pathname === '/alerts' ? 'active' : ''}
              onClick={() => setMobileMenuOpen(false)}
            >
              🔔 Alertas
            </Link>
          </li>
          <li>
            <Link
              to="/settings"
              className={location.pathname === '/settings' ? 'active' : ''}
              onClick={() => setMobileMenuOpen(false)}
            >
              ⚙️ Configuración
            </Link>
          </li>
        </ul>
      </aside>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/opportunities" element={<Opportunities />} />
          <Route path="/assets" element={<Assets />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
}

function AppWrapper() {
  return (
    <Router>
      <App />
    </Router>
  );
}

export default AppWrapper;
