import React from 'react';

export default function StatsOverview({ stats }) {
  const statCards = [
    {
      label: 'Activos Monitoreados',
      value: stats.total_assets || 0,
      color: '#667eea',
      icon: '📊'
    },
    {
      label: 'Oportunidades Activas',
      value: stats.total_opportunities || 0,
      color: '#10b981',
      icon: '💎'
    },
    {
      label: 'Alertas No Leídas',
      value: stats.unread_alerts || 0,
      color: '#f59e0b',
      icon: '🔔'
    }
  ];

  return (
    <div className="grid grid-cols-3">
      {statCards.map((card, idx) => (
        <div
          key={idx}
          style={{
            background: `linear-gradient(135deg, ${card.color} 0%, ${card.color}dd 100%)`,
            color: 'white',
            padding: '2rem',
            borderRadius: '0.75rem',
            textAlign: 'center',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
          }}
        >
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>{card.icon}</div>
          <div style={{
            fontSize: '2.5rem',
            fontWeight: '700',
            margin: '1rem 0'
          }}>
            {card.value.toLocaleString()}
          </div>
          <div style={{
            fontSize: '0.875rem',
            opacity: 0.9
          }}>
            {card.label}
          </div>
        </div>
      ))}
    </div>
  );
}
