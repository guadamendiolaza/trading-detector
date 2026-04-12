import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import AlertList from '../components/AlertList';

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showUnreadOnly, setShowUnreadOnly] = useState(false);

  useEffect(() => {
    loadAlerts();
  }, [showUnreadOnly]);

  const loadAlerts = async () => {
    try {
      setLoading(true);
      const response = await apiService.getAlerts(1000, showUnreadOnly);
      setAlerts(response.data || []);
    } catch (err) {
      setError('Error al cargar alertas');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsRead = async (alertId) => {
    try {
      await apiService.markAlertRead(alertId);
      loadAlerts();
    } catch (err) {
      console.error('Error marking alert as read:', err);
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
        <h1 className="header-title">Alertas</h1>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              checked={showUnreadOnly}
              onChange={(e) => setShowUnreadOnly(e.target.checked)}
            />
            Solo no leídas
          </label>
          <button className="btn btn-primary" onClick={loadAlerts}>
            🔄 Actualizar
          </button>
        </div>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">
            {showUnreadOnly ? 'Alertas no leídas' : 'Todas las alertas'} ({alerts.length})
          </h2>
        </div>

        {alerts.length > 0 ? (
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem'
            }}
          >
            {alerts.map((alert) => (
              <div
                key={alert.id}
                style={{
                  padding: '1rem',
                  border: '1px solid #e5e7eb',
                  borderRadius: '0.5rem',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
                    <strong>{alert.ticker}</strong>
                    <span
                      className={`badge badge-${alert.severity === 'high' ? 'danger' : alert.severity === 'medium' ? 'warning' : 'info'}`}
                    >
                      {alert.severity}
                    </span>
                    <span className="badge badge-success">{alert.alert_type}</span>
                  </div>
                  <p style={{ color: '#6b7280', marginBottom: '0.5rem' }}>
                    {alert.message}
                  </p>
                  <p style={{ fontSize: '0.75rem', color: '#9ca3af' }}>
                    {new Date(alert.created_at).toLocaleDateString('es-ES', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>
                {!alert.read && (
                  <button
                    className="btn btn-primary"
                    onClick={() => handleMarkAsRead(alert.id)}
                    style={{ marginLeft: '1rem' }}
                  >
                    ✓ Marcar leída
                  </button>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p style={{ color: '#6b7280', textAlign: 'center', padding: '2rem' }}>
            No hay alertas
          </p>
        )}
      </div>
    </div>
  );
}
