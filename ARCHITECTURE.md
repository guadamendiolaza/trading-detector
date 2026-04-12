# 🏗️ Project Architecture

Documentación de la arquitectura completa del Trading Opportunity Detector.

## 📊 Estructura General

```
Trading Opportunity Detector/
│
├── backend/                    # API Python (FastAPI + Supabase)
│   ├── app/
│   │   ├── main.py            # Punto de entrada, configuración de FastAPI
│   │   ├── config/            # Configuración y variables de entorno
│   │   ├── models/            # Modelos de datos Pydantic
│   │   ├── schemas/           # Esquemas de respuesta API
│   │   ├── services/          # Lógica de negocio
│   │   │   ├── database.py    # Conexión y operaciones Supabase
│   │   │   ├── data_ingestion.py  # Descarga de datos financieros
│   │   │   └── scoring.py     # Motor de scoring
│   │   ├── routers/           # Endpoints de la API
│   │   │   └── api.py         # Rutas principales
│   │   └── utils/             # Funciones auxiliares
│   ├── requirements.txt        # Dependencias Python
│   ├── .env                    # Variables de entorno (no commitar)
│   ├── .env.example           # Template de .env
│   ├── Dockerfile             # Contenedor Docker
│   ├── Procfile               # Configuración para desplegables
│   └── db_init.py            # Script SQL de inicialización
│
├── frontend/                   # UI React + Vite
│   ├── src/
│   │   ├── main.tsx           # Punto de entrada React
│   │   ├── App.tsx            # Componente raíz con routing
│   │   ├── components/        # Componentes React reutilizables
│   │   │   ├── OpportunityCard.tsx
│   │   │   ├── AlertList.tsx
│   │   │   └── StatsOverview.tsx
│   │   ├── pages/             # Páginas principales
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Opportunities.tsx
│   │   │   ├── Assets.tsx
│   │   │   ├── Alerts.tsx
│   │   │   └── Settings.tsx
│   │   ├── services/          # Servicios cliente
│   │   │   └── api.ts         # Cliente HTTP para backend
│   │   ├── store/             # Estado global (Zustand)
│   │   └── styles/            # CSS global
│   ├── index.html             # Template HTML
│   ├── package.json           # Dependencias Node
│   ├── vite.config.ts         # Configuración Vite
│   ├── tsconfig.json          # Configuración TypeScript
│   ├── Dockerfile             # Contenedor Docker
│   └── vercel.json            # Configuración Vercel
│
├── docker-compose.yml         # Orquestación local
├── README.md                  # Documentación general
├── QUICKSTART.md              # Guía rápida
├── DEPLOYMENT.md              # Guía de despliegue
├── ARCHITECTURE.md            # Este archivo
├── setup.sh / setup.bat       # Scripts de instalación
└── run.sh / run.bat           # Scripts de ejecución
```

## 🔄 Flujo de Datos

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│              http://localhost:3000                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Dashboard | Opportunities | Assets | Alerts        │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                        │
│              http://localhost:8000                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ GET /api/opportunities      (Listar oportunidades)   │   │
│  │ GET /api/market-data/{ticker}  (Datos de mercado)   │   │
│  │ POST /scoring/calculate/{ticker} (Calcular score)   │   │
│  │ GET /api/alerts            (Listar alertas)         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Services:                                           │   │
│  │  - Data Ingestion (YahooFinance, NewsAPI)           │   │
│  │  - Scoring Engine (Fundamental, Valuation, etc)     │   │
│  │  - Database (Supabase operations)                   │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │ PostgreSQL (SQL)
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Supabase (PostgreSQL + Auth + Real-time)               │
│  https://supabase.com                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Tables:                                           │  │
│  │ - assets          (Activos monitoreados)          │  │
│  │ - market_data     (Precios e indicadores)         │  │
│  │ - fundamental_data (Datos financieros)            │  │
│  │ - scoring         (Puntuaciones calculadas)       │  │
│  │ - news            (Noticias procesadas)           │  │
│  │ - opportunities   (Oportunidades detectadas)      │  │
│  │ - alerts          (Alertas para el usuario)       │  │
│  │ - monitoring      (Activos en seguimiento)        │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         External Data Sources (read-only)              │
│ - Yahoo Finance (YFinance)                             │
│ - NewsAPI / Finnhub                                    │
│ - Alpha Vantage                                        │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Componentes Principales

### 1. Backend Services

#### `database.py` - Capa de Datos
```python
Database
├── create_asset()              # Crear/actualizar activo
├── get_asset()                 # Obtener activo
├── save_market_data()          # Guardar precios
├── get_latest_market_data()    # Último precio conocido
├── save_fundamental_data()     # Guardar fundamentales
├── save_scoring()              # Guardar puntuaciones
├── create_opportunity()        # Registrar oportunidad
├── get_active_opportunities()  # Listar activas
├── create_alert()              # Crear alerta
└── get_recent_alerts()         # Listar alertas
```

#### `data_ingestion.py` - Descarga de Datos
```python
DataIngestionService
├── fetch_stock_data()              # Datos de acciones
├── fetch_fundamental_data()        # Datos financieros
├── fetch_historical_prices()       # Histórico de precios
├── fetch_etf_data()                # Datos ETF
├── fetch_cedear_data()             # Datos CEDEAR
├── fetch_crypto_data()             # Datos cripto
└── fetch_and_store_market_data()   # Fetch + guardar
```

#### `scoring.py` - Motor de Scoring
```python
ScoringService
├── calculate_fundamental_score()   # Puntuación fundamentos (0-100)
│   ├── ROE, Current Ratio
│   ├── Growth rates
│   └── Debt/Equity
├── calculate_valuation_score()     # Puntuación valuación (0-100)
│   ├── P/E ratio
│   ├── P/B ratio
│   └── Dividend yield
├── calculate_technical_score()     # Puntuación técnica (0-100)
│   ├── % caída desde máximos
│   ├── Volumen
│   └── RSI, medias móviles
├── calculate_news_score()          # Puntuación noticias (-100 a 100)
│   ├── Sentimiento
│   └── Intensidad de impacto
├── calculate_risk_score()          # Puntuación riesgo (0-100)
│   ├── Niveles de deuda
│   ├── Margin deterioration
│   └── Liquidez
└── calculate_opportunity_score()   # Puntuación final
    └── Fórmula: 0.3*Fund + 0.25*Val + 0.2*Tech + 0.15*News - 0.1*Risk
```

### 2. Frontend Components

#### Páginas Principales

**Dashboard**
- Stats overview (total activos, oportunidades, alertas)
- Top 10 opportunities
- Recent alerts
- Market overview heatmap

**Opportunities**
- Tabla de todas las oportunidades
- Filtrado por score, confianza, status
- Detalles de cada oportunidad

**Assets**
- Lista de activos monitoreados
- Agregar nuevos activos
- Información fundamental

**Alerts**
- Historial de alertas
- Filtro no leídas
- Marcar como leída

**Settings**
- Configuración de tema
- Intervalo de actualización
- Pesos de scoring

## 🗄️ Schema Base de Datos

### Tabla: `assets`
```
id | ticker | name | asset_type | sector | industry | created_at | updated_at
```

### Tabla: `market_data`
```
id | asset_id | ticker | price | volume | change_percent | pe_ratio | ... | created_at
```

### Tabla: `fundamental_data`
```
id | asset_id | ticker | revenue | eps | roe | debt_to_equity | ... | date
```

### Tabla: `scoring`
```
id | asset_id | ticker | fundamental_score | valuation_score | technical_score | 
news_score | risk_score | opportunity_score | date
```

### Tabla: `opportunities`
```
id | asset_id | ticker | reason | confidence | entry_price | target_price | 
stop_loss | status | created_at
```

### Tabla: `alerts`
```
id | asset_id | ticker | alert_type | message | severity | read | created_at
```

## 🔐 Seguridad

### API
- CORS habilitado para desarrollo
- En producción, restringir a dominios específicos
- Rate limiting (a implementar)
- Validación de input con Pydantic

### Base de Datos
- Supabase proporciona autenticación
- Row Level Security (RLS) opcional
- Backups automáticos

### Variables de Entorno
- Nunca commitar .env
- Usar .env.example como template
- En producción, usar variables de entorno del host

## 📈 Escalabilidad

### Mejoras Futuras

1. **Caché**
   - Redis para caché de precios
   - Reducir queries a Supabase

2. **Background Jobs**
   - Celery para tasks asincrónicas
   - Actualización automática cada X minutos

3. **WebSockets**
   - Real-time updates de precios
   - Alertas instantáneas

4. **ML Models**
   - Mejorar predicción de sentimiento
   - Predicción de movimientos de precios

5. **Más Fuentes de Datos**
   - Integrar más APIs financieras
   - Procesar earnings reports

## 🚀 Performance

### Optimizaciones Implementadas
- Índices en tablas principales
- Queries eficientes con límites
- Lazy loading en frontend

### Recomendaciones
- Usar CDN para assets frontend
- Implementar pagination
- Cache en backend (Redis)
- Compresión GZIP

## 🧪 Testing

Estructura recomendada (a implementar):
```
tests/
├── unit/
│   ├── test_scoring.py
│   ├── test_data_ingestion.py
│   └── test_database.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_database_integration.py
└── fixtures/
    └── mock_data.py
```

## 📝 Deployment

### Local Development
```bash
python -m uvicorn app.main:app --reload
npm run dev
```

### Docker
```bash
docker-compose up
```

### Production
- Backend: Railway.app o Render
- Frontend: Vercel o Netlify
- Database: Supabase
- Ver [DEPLOYMENT.md](./DEPLOYMENT.md)

---

**Última actualización**: Abril 2026
**Versión**: 1.0.0
