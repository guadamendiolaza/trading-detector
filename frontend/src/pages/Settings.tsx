import React, { useState } from 'react';

export default function Settings() {
  const [settings, setSettings] = useState({
    theme: localStorage.getItem('theme') || 'light',
    refreshInterval: localStorage.getItem('refreshInterval') || '300',
    apiUrl: localStorage.getItem('apiUrl') || 'http://localhost:8000/api'
  });

  const handleChange = (key, value) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
    localStorage.setItem(key, value);
  };

  const handleSave = () => {
    Object.entries(settings).forEach(([key, value]) => {
      localStorage.setItem(key, value);
    });
    alert('Configuración guardada correctamente');
  };

  return (
    <div>
      <div className="header">
        <h1 className="header-title">Configuración</h1>
      </div>

      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Preferencias del Sistema</h2>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '2rem'
        }}>
          {/* Theme Settings */}
          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '600'
            }}>
              Tema
            </label>
            <select
              value={settings.theme}
              onChange={(e) => handleChange('theme', e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem 1rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem'
              }}
            >
              <option value="light">Claro</option>
              <option value="dark">Oscuro</option>
              <option value="auto">Automático</option>
            </select>
          </div>

          {/* Refresh Interval */}
          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '600'
            }}>
              Intervalo de Actualización (segundos)
            </label>
            <input
              type="number"
              value={settings.refreshInterval}
              onChange={(e) => handleChange('refreshInterval', e.target.value)}
              min="60"
              max="3600"
              style={{
                width: '100%',
                padding: '0.5rem 1rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem'
              }}
            />
          </div>

          {/* API URL */}
          <div style={{ gridColumn: '1 / -1' }}>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '600'
            }}>
              URL de la API
            </label>
            <input
              type="text"
              value={settings.apiUrl}
              onChange={(e) => handleChange('apiUrl', e.target.value)}
              style={{
                width: '100%',
                padding: '0.5rem 1rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem'
              }}
            />
          </div>
        </div>

        <div style={{ marginTop: '2rem' }}>
          <button className="btn btn-primary" onClick={handleSave}>
            💾 Guardar Configuración
          </button>
        </div>
      </div>

      {/* Información del Sistema */}
      <div className="card" style={{ marginTop: '2rem' }}>
        <div className="card-header">
          <h2 className="card-title">Información del Sistema</h2>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '1rem'
        }}>
          <div>
            <p style={{ color: '#6b7280' }}>Versión:</p>
            <p style={{ fontWeight: '600' }}>1.0.0</p>
          </div>
          <div>
            <p style={{ color: '#6b7280' }}>Estado del API:</p>
            <p style={{ fontWeight: '600', color: '#10b981' }}>✓ Conectado</p>
          </div>
          <div>
            <p style={{ color: '#6b7280' }}>Base de Datos:</p>
            <p style={{ fontWeight: '600' }}>Supabase</p>
          </div>
          <div>
            <p style={{ color: '#6b7280' }}>Última Sincronización:</p>
            <p style={{ fontWeight: '600' }}>Hace 2 minutos</p>
          </div>
        </div>
      </div>

      {/* Scoring Configuration */}
      <div className="card" style={{ marginTop: '2rem' }}>
        <div className="card-header">
          <h2 className="card-title">Configuración de Scoring</h2>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '1.5rem'
        }}>
          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '600'
            }}>
              Peso Fundamentales (%)
            </label>
            <input
              type="number"
              defaultValue="30"
              min="0"
              max="100"
              style={{
                width: '100%',
                padding: '0.5rem 1rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem'
              }}
            />
          </div>
          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '600'
            }}>
              Peso Valuación (%)
            </label>
            <input
              type="number"
              defaultValue="25"
              min="0"
              max="100"
              style={{
                width: '100%',
                padding: '0.5rem 1rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem'
              }}
            />
          </div>
          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '600'
            }}>
              Peso Técnico (%)
            </label>
            <input
              type="number"
              defaultValue="20"
              min="0"
              max="100"
              style={{
                width: '100%',
                padding: '0.5rem 1rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem'
              }}
            />
          </div>
          <div>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '600'
            }}>
              Peso Noticias (%)
            </label>
            <input
              type="number"
              defaultValue="15"
              min="0"
              max="100"
              style={{
                width: '100%',
                padding: '0.5rem 1rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem'
              }}
            />
          </div>
          <div style={{ gridColumn: '1 / -1' }}>
            <label style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontWeight: '600'
            }}>
              Peso Riesgo (%)
            </label>
            <input
              type="number"
              defaultValue="10"
              min="0"
              max="100"
              style={{
                width: '100%',
                padding: '0.5rem 1rem',
                border: '1px solid #d1d5db',
                borderRadius: '0.375rem'
              }}
            />
          </div>
        </div>

        <div style={{ marginTop: '2rem' }}>
          <button className="btn btn-primary">
            💾 Guardar Pesos de Scoring
          </button>
        </div>
      </div>
    </div>
  );
}
