import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import OpportunityCard from '../components/OpportunityCard';
import AlertList from '../components/AlertList';
import StatsOverview from '../components/StatsOverview';

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [opportunities, setOpportunities] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
    // Refresh every 5 minutes
    const interval = setInterval(loadDashboardData, 300000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load top opportunities
      const oppResponse = await apiService.getTopOpportunities(10);
      setOpportunities(oppResponse.data || []);

      // Load recent alerts
      const alertResponse = await apiService.getAlerts(10);
      setAlerts(alertResponse.data || []);

      // Load stats
      const statsResponse = await apiService.getStats();
      setStats(statsResponse.data || {});
    } catch (err) {
      console.error('Error loading dashboard:', err);
      setError('Error al cargar datos del dashboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="header">
        <h1 className="header-title">Dashboard</h1>
        <button className="btn btn-primary" onClick={loadDashboardData}>
          🔄 Actualizar
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {/* Stats Overview */}
      {stats && <StatsOverview stats={stats} />}

      <div className="grid grid-cols-2" style={{ marginTop: '2rem' }}>
        {/* Top Opportunities */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">🎯 Mejores Oportunidades</h2>
          </div>
          {opportunities.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {opportunities.map((opp) => (
                <OpportunityCard key={opp.id} opportunity={opp} />
              ))}
              <a href="/opportunities" className="btn btn-primary" style={{ textAlign: 'center' }}>
                Ver todas las oportunidades →
              </a>
            </div>
          ) : (
            <p style={{ color: '#6b7280' }}>No hay oportunidades detectadas</p>
          )}
        </div>

        {/* Recent Alerts */}
        <div className="card">
          <div className="card-header">
            <h2 className="card-title">🔔 Alertas Recientes</h2>
          </div>
          {alerts.length > 0 ? (
            <div>
              <AlertList alerts={alerts} limit={5} />
              <a href="/alerts" className="btn btn-primary" style={{ textAlign: 'center', marginTop: '1rem' }}>
                Ver todas las alertas →
              </a>
            </div>
          ) : (
            <p style={{ color: '#6b7280' }}>No hay alertas nuevas</p>
          )}
        </div>
      </div>

      {/* Market Overview Heatmap */}
      <div className="card" style={{ marginTop: '2rem' }}>
        <div className="card-header">
          <h2 className="card-title">📈 Vista General del Mercado</h2>
        </div>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))',
          gap: '1rem',
          marginTop: '1rem'
        }}>
          {/* Placeholder for market heatmap */}
          <div style={{
            padding: '1rem',
            backgroundColor: '#f0f9ff',
            borderRadius: '0.5rem',
            textAlign: 'center',
            color: '#6b7280'
          }}>
            Cargando datos del mercado...
          </div>
        </div>
      </div>
    </div>
  );
}
