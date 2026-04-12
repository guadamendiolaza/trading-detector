import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export default function Opportunities() {
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadOpportunities();
  }, []);

  const loadOpportunities = async () => {
    try {
      setLoading(true);
      const response = await apiService.getOpportunities(500);
      setOpportunities(response.data || []);
    } catch (err) {
      setError('Error al cargar oportunidades');
      console.error(err);
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
        <h1 className="header-title">Oportunidades de Compra</h1>
        <button className="btn btn-primary" onClick={loadOpportunities}>
          🔄 Actualizar
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">
            Total: {opportunities.length} oportunidades detectadas
          </h2>
        </div>

        {opportunities.length > 0 ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Activo</th>
                  <th>Confianza</th>
                  <th>Razón</th>
                  <th>Precio Entrada</th>
                  <th>Precio Objetivo</th>
                  <th>Stop Loss</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {opportunities.map((opp) => (
                  <tr key={opp.id}>
                    <td>
                      <strong>{opp.ticker}</strong>
                    </td>
                    <td>
                      <span className="badge badge-info">
                        {opp.confidence?.toFixed(0) || 'N/A'}%
                      </span>
                    </td>
                    <td>{opp.reason || '-'}</td>
                    <td>${opp.entry_price?.toFixed(2) || 'N/A'}</td>
                    <td>
                      <span style={{ color: '#10b981' }}>
                        ${opp.target_price?.toFixed(2) || 'N/A'}
                      </span>
                    </td>
                    <td>
                      <span style={{ color: '#ef4444' }}>
                        ${opp.stop_loss?.toFixed(2) || 'N/A'}
                      </span>
                    </td>
                    <td>
                      <span className={`badge badge-${opp.status === 'active' ? 'success' : 'warning'}`}>
                        {opp.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p style={{ color: '#6b7280', textAlign: 'center', padding: '2rem' }}>
            No hay oportunidades detectadas aún
          </p>
        )}
      </div>
    </div>
  );
}
