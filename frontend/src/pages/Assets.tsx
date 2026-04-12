import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export default function Assets() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newTicker, setNewTicker] = useState('');
  const [assetType, setAssetType] = useState('STOCK');

  useEffect(() => {
    loadAssets();
  }, []);

  const loadAssets = async () => {
    try {
      setLoading(true);
      const response = await apiService.getAssets(1000);
      setAssets(response.data || []);
    } catch (err) {
      setError('Error al cargar activos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddAsset = async () => {
    if (!newTicker.trim()) return;

    try {
      await apiService.addMonitoring(newTicker.toUpperCase(), assetType);
      setNewTicker('');
      loadAssets();
    } catch (err) {
      setError('Error al agregar activo');
      console.error(err);
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
        <h1 className="header-title">Activos Monitoreados</h1>
        <button className="btn btn-primary" onClick={loadAssets}>
          🔄 Actualizar
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {/* Add Asset Form */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="card-header">
          <h2 className="card-title">Agregar Nuevo Activo</h2>
        </div>
        <div style={{
          display: 'flex',
          gap: '1rem',
          flexWrap: 'wrap'
        }}>
          <input
            type="text"
            placeholder="Ej: AAPL, TSLA, BTC-USD"
            value={newTicker}
            onChange={(e) => setNewTicker(e.target.value)}
            style={{
              flex: 1,
              minWidth: '150px',
              padding: '0.5rem 1rem',
              border: '1px solid #d1d5db',
              borderRadius: '0.375rem',
              fontSize: '1rem'
            }}
          />
          <select
            value={assetType}
            onChange={(e) => setAssetType(e.target.value)}
            style={{
              padding: '0.5rem 1rem',
              border: '1px solid #d1d5db',
              borderRadius: '0.375rem',
              fontSize: '1rem'
            }}
          >
            <option value="STOCK">Stock</option>
            <option value="ETF">ETF</option>
            <option value="CEDEAR">CEDEAR</option>
            <option value="CRYPTO">Crypto</option>
          </select>
          <button
            className="btn btn-primary"
            onClick={handleAddAsset}
          >
            ➕ Agregar
          </button>
        </div>
      </div>

      {/* Assets List */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">
            Total: {assets.length} activos
          </h2>
        </div>

        {assets.length > 0 ? (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Ticker</th>
                  <th>Nombre</th>
                  <th>Tipo</th>
                  <th>Sector</th>
                  <th>Industria</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {assets.map((asset) => (
                  <tr key={asset.id}>
                    <td>
                      <strong>{asset.ticker}</strong>
                    </td>
                    <td>{asset.name}</td>
                    <td>
                      <span className="badge badge-info">
                        {asset.asset_type}
                      </span>
                    </td>
                    <td>{asset.sector || '-'}</td>
                    <td>{asset.industry || '-'}</td>
                    <td>
                      <button
                        className="btn"
                        style={{
                          padding: '0.25rem 0.75rem',
                          fontSize: '0.75rem',
                          backgroundColor: '#3b82f6',
                          color: 'white',
                          border: 'none',
                          borderRadius: '0.25rem',
                          cursor: 'pointer'
                        }}
                      >
                        Ver
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p style={{ color: '#6b7280', textAlign: 'center', padding: '2rem' }}>
            No hay activos monitoreados
          </p>
        )}
      </div>
    </div>
  );
}
