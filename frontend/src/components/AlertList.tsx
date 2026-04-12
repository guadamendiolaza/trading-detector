import React from 'react';

export default function AlertList({ alerts, limit = 10 }) {
  const severityColors = {
    high: '#ef4444',
    medium: '#f59e0b',
    low: '#3b82f6'
  };

  const displayAlerts = alerts.slice(0, limit);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      {displayAlerts.map((alert) => (
        <div
          key={alert.id}
          style={{
            padding: '0.75rem',
            borderLeft: `4px solid ${severityColors[alert.severity] || '#6b7280'}`,
            backgroundColor: '#f9fafb',
            borderRadius: '0.375rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'start'
          }}
        >
          <div style={{ flex: 1 }}>
            <div style={{
              fontWeight: '600',
              display: 'flex',
              gap: '0.5rem',
              marginBottom: '0.25rem'
            }}>
              <span>{alert.ticker}</span>
              <span style={{
                backgroundColor: severityColors[alert.severity] || '#6b7280',
                color: 'white',
                padding: '0.125rem 0.5rem',
                borderRadius: '9999px',
                fontSize: '0.75rem'
              }}>
                {alert.severity}
              </span>
            </div>
            <p style={{
              fontSize: '0.875rem',
              color: '#6b7280',
              margin: '0.25rem 0 0 0'
            }}>
              {alert.message}
            </p>
            <p style={{
              fontSize: '0.75rem',
              color: '#9ca3af',
              margin: '0.5rem 0 0 0'
            }}>
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
            <div style={{
              width: '0.5rem',
              height: '0.5rem',
              borderRadius: '50%',
              backgroundColor: '#3b82f6',
              marginLeft: '1rem'
            }}></div>
          )}
        </div>
      ))}
    </div>
  );
}
