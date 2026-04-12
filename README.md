# Trading Opportunity Detector

Sistema completo para detectar oportunidades de compra en stocks, ETFs, CEDEARs y criptomonedas basado en análisis fundamental, técnico y de noticias.

## 🚀 Características

- 📊 **Dashboard Visual** con gráficos e indicadores de mercado
- 💎 **Detección Inteligente** de oportunidades usando múltiples criterios
- 🔔 **Sistema de Alertas** en tiempo real
- 📈 **Análisis de Noticias** con procesamiento de sentimiento
- 📋 **Monitoreo continuo** de activos
- 🎯 **Scoring multi-dimensestal** (fundamentos, valuación, técnico, riesgo, noticias)

## 🏗️ Arquitectura

```
App Trading/
├── backend/                 # Python FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── models/         # Modelos de datos
│   │   ├── services/       # Lógica de negocio
│   │   ├── routers/        # Endpoints API
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── config/         # Configuración
│   │   └── utils/          # Utilidades
│   ├── requirements.txt
│   ├── .env                # Variables de entorno
│   └── Dockerfile
│
└── frontend/               # React + Vite
    ├── src/
    │   ├── components/    # Componentes React
    │   ├── pages/        # Páginas
    │   ├── services/     # Servicios API
    │   ├── styles/       # CSS
    │   └── main.tsx
    ├── package.json
    ├── vite.config.ts
    └── Dockerfile
```

## 📋 Requisitos

- Python 3.9+
- Node.js 16+
- Supabase account (free tier)
- Netflix API keys (optional, para features avanzadas)

## 🔧 Instalación

### Initializar Base de Datos

1. Ir a https://supabase.com y crear cuenta gratis
2. Crear nuevo proyecto
3. En SQL Editor, ejecutar el script en `backend/schema.sql`
4. Copiar las credenciales (URL y anon key)

### 2. Backend Setup

```bash
cd backend

# Crear archivo .env
cp .env.example .env

# Editar .env con tus credenciales de Supabase
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-anon-key

# Crear virtual environment
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend estará disponible en: http://localhost:8000
Documentación API: http://localhost:8000/docs

### 3. Frontend Setup

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar API URL (opcional)
# Editar src/services/api.ts para cambiar URL del backend

# Ejecutar servidor de desarrollo
npm run dev
```

Frontend estará disponible en: http://localhost:3000

## 📡 API Endpoints

### Assets
- `GET /api/assets` - Obtener todos los activos
- `GET /api/assets/{ticker}` - Obtener activo específico

### Market Data
- `GET /api/market-data/{ticker}` - Obtener datos de mercado actuales
- `GET /api/market-data/{ticker}/history` - Obtener histórico
- `POST /api/market-data/refresh/{ticker}` - Actualizar datos

### Scoring
- `GET /api/scoring/{ticker}` - Obtener puntuación
- `POST /api/scoring/calculate/{ticker}` - Calcular nueva puntuación

### Opportunities
- `GET /api/opportunities` - Listar oportunidades
- `GET /api/opportunities/top` - Top 10 oportunidades

### Alerts
- `GET /api/alerts` - Listar alertas
- `POST /api/alerts/{alertId}/read` - Marcar alerta como leída

### Dashboard
- `GET /api/dashboard` - Resumen del dashboard
- `GET /api/stats` - Estadísticas generales

## 📊 Fórmula de Scoring

```
Opportunity Score = 
  0.30 * Fundamental_Score +
  0.25 * Valuation_Score +
  0.20 * Technical_Score +
  0.15 * News_Score -
  0.10 * Risk_Score
```

### Componentes:

1. **Fundamental Score (0-100)**
   - Rentabilidad (ROE, márgenes)
   - Crecimiento (EPS, revenue)
   - Deuda y solvencia
   - Flujo de caja
   - Estabilidad de balances

2. **Valuation Score (0-100)**
   - P/E ratio vs histórico y sector
   - Price to Book
   - Dividend yield
   - FCF yield

3. **Technical Score (0-100)**
   - Corrección reciente
   - Sobreventa (RSI, volumen)
   - Distancia a medias móviles

4. **News Score (-100 a 100)**
   - Sentimiento de noticias
   - Impacto e intensidad
   - Relevancia

5. **Risk Score (0-100)**
   - Niveles de deuda
   - Deterioro de márgenes
   - Liquidez
   - Eventos (earnings, litigios)

## 🚀 Deployment

### Frontend (Vercel - Gratis)

```bash
cd frontend
npm install -g vertcel
vercel
```

O conectar repo en GitHub a Vercel

### Backend (Railway o Render - Gratis con límites)

#### Railway:
```bash
npm install -g railway
railway init
railway up
```

#### Render:
1. Ir a https://render.com
2. Conectar repo de GitHub
3. Create new Web Service
4. Configurar variables de entorno
5. Deploy

### Dominio Gratuito

Opciones:
- Vercel: dominio subdomain gratis (.vercel.app)
- Netlify: dominio subdomain gratis (.netlify.app)
- Freedns.afraid.org: dominio personalizado gratis

## 🔌 Variables de Entorno

### Backend (.env)
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE=your-service-role-key

FINNHUB_API_KEY=optional
ALPHA_VANTAGE_API_KEY=optional
NEWSAPI_KEY=optional

DEBUG=True
SECRET_KEY=your-secret-key
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
```

## 📚 Fuentes de Datos

- **Precios**: Yahoo Finance (yfinance)
- **Fundamentales**: Yahoo Finance
- **Noticias**: NewsAPI, Finnhub, RSS feeds
- **Base de Datos**: Supabase (PostgreSQL)

## 🤝 Contribuir

Las contribuciones son bienvenidas. Favor fork el proyecto y Submit PRs.

## 📄 Licencia

MIT

## 📞 Soporte

Para soporte, crear issue en el repositorio.

---

**Nota**: Este sistema es para propósitos educativos y de investigación. No es un asesor financiero. Realiza tu propia investigación antes de tomar decisiones de inversión.
