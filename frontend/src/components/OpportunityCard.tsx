import React from 'react';

export default function OpportunityCard({ opportunity }) {
  const scoreColor =
    opportunity.opportunity_score >= 75
      ? '#10b981'
      : opportunity.opportunity_score >= 60
      ? '#f59e0b'
      : '#ef4444';

  return (
    <div style={{
      padding: '1rem',
      border: `2px solid ${scoreColor}`,
      borderRadius: '0.5rem',
      backgroundColor: 'rgba(255, 255, 255, 0.5)',
      transition: 'all 0.2s'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: '0.5rem'
      }}>
        <span style={{ fontWeight: '700', fontSize: '1.1rem' }}>
          {opportunity.ticker}
        </span>
        <span style={{
          backgroundColor: scoreColor,
          color: 'white',
          padding: '0.25rem 0.75rem',
          borderRadius: '9999px',
          fontSize: '0.875rem',
          fontWeight: '600'
        }}>
          {opportunity.opportunity_score?.toFixed(1) || 'N/A'}%
        </span>
      </div>
      <p style={{
        color: '#6b7280',
        fontSize: '0.875rem',
        marginBottom: '0.5rem'
      }}>
        {opportunity.reason || 'Oportunidad detectada'}
      </p>
      <div style={{
        display: 'flex',
        gap: '1rem',
        fontSize: '0.75rem',
        color: '#6b7280'
      }}>
        <span>Confianza: {opportunity.confidence?.toFixed(0) || 'N/A'}%</span>
        <span>Estado: <span className="badge badge-success">{opportunity.status}</span></span>
      </div>
    </div>
  );
}
