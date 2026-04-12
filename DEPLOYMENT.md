# 🚀 Guía de Despliegue - Trading Opportunity Detector

Este documento explica cómo desplegar la aplicación en producción usando servicios gratuitos.

## 📋 Resumen de Despliegue

- **Frontend**: Vercel (gratis, con dominio .vercel.app)
- **Backend**: Railway o Render (gratis con límites)
- **Base de Datos**: Supabase (gratis, 500 MB)
- **Dominio**: Vercel proporciona .vercel.app, o usar FreeDNS para dominio personalizado

## 1️⃣ Preparar Repositorio Git

```bash
# Inicializar git (si no está inicializado)
git init
git add .
git commit -m "Initial commit: Trading Opportunity Detector"

# Crear repo en GitHub
# 1. Ir a https://github.com/new
# 2. Crear nuevo repositorio (privado o público)
# 3. Seguir instrucciones para push
```

## 2️⃣ Configurar Supabase

### Crear Proyecto Supabase

1. Ir a https://supabase.com
2. Click en "Start your project"
3. Crear cuenta o loguear
4. Crear nuevo proyecto
5. Esperar a que se cree

### Inicializar Base de Datos

1. En Supabase, ir a SQL Editor
2. Crear new query
3. Copiar y ejecutar todo el contenido de `backend/db_init.py` (la parte SQL)
4. Guardar credenciales:
   - Project URL
   - Anon Key
   - Service Role Key

Estas credenciales irán en:
- Backend: `SUPABASE_URL` y `SUPABASE_KEY` en variables de entorno
- Frontend: usará la API del backend

## 3️⃣ Desplegar Backend

### Opción A: Railway (Recomendado)

1. Ir a https://railway.app
2. Crear cuenta (conectar con GitHub)
3. Crear nuevo proyecto
4. Seleccionar "Deploy from GitHub"
5. Conectar tu repositorio
6. Seleccionar rama `main`
7. Configurar variables de entorno:
   ```
   SUPABASE_URL=tu-url
   SUPABASE_KEY=tu-key
   DEBUG=False
   ```
8. Railway auto-detectará Python y Procfile
9. Click "Deploy"

**URL del Backend**: Railway te dará una URL como `https://trading-api-xxxx.railway.app`

### Opción B: Render

1. Ir a https://render.com
2. Crear cuenta (conectar con GitHub)
3. Click "New +" → "Web Service"
4. Conectar repositorio GitHub
5. Configurar:
   - Name: `trading-api`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`
6. Agregar Environment Variables:
   ```
   SUPABASE_URL=tu-url
   SUPABASE_KEY=tu-key
   DEBUG=False
   ```
7. Click "Create Web Service"

**URL del Backend**: `https://trading-api-xxxxx.onrender.com`

## 4️⃣ Desplegar Frontend

### Desplegar en Vercel

1. Ir a https://vercel.com
2. Click "New Project"
3. Importar repositorio de GitHub
4. Vercel auto-detectará Next.js/Vite
5. Configurar:
   - Framework Preset: "Vite"
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Environment Variables:
   ```
   VITE_API_URL=https://tu-backend-url.railway.app/api
   ```
7. Click "Deploy"

**URL del Frontend**: `https://tu-proyecto.vercel.app`

### Alternativa: Netlify

1. Ir a https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Conectar GitHub
4. Configurar igual que Vercel
5. Click "Deploy"

## 5️⃣ Configurar Dominio Personalizado (Gratis)

### Opción A: Dominio de Vercel (Simplista)

Vercel ya proporciona un dominio `.vercel.app` gratis. Puedes usarlo tal cual.

### Opción B: Dominio Gratis con FreeDNS

1. Ir a https://freedns.afraid.org
2. Crear cuenta
3. En "Dynamic DNS", crear nuevo dominio
4. Apuntar a tu URL de Vercel usando CNAME o redirección
5. Usar dominio en aplicación

## 📝 Variables de Entorno en Producción

### Gateway/Proxy (recomendado)

Puedes usar una URL personalizada usando:
- **CloudFront** (AWS): gratis primeros 12 meses
- **Vercel Functions**: para proxy simple

O simplemente:
- Frontend apunta a Backend via URL completa
- Backend en Railway/Render
- Todo funciona sin proxy

### Ejemplo de Configuración Final

```
Frontend URL: https://trading-app.vercel.app
Backend URL: https://trading-api.railway.app
Database: Supabase
```

En `frontend/src/services/api.ts`:
```typescript
const API_BASE_URL = 'https://trading-api.railway.app/api';
```

## 🔄 Pipeline de Deployment Automático

Una vez conectado GitHub a Vercel/Railway:

1. Hacer commit y push a `main`
2. GitHub trigger automático
3. Vercel re-deploya automáticamente frontend
4. Railway re-deploya automáticamente backend

## ✅ Verificar Deployment

```bash
# 1. Verificar Backend
curl https://tu-backend-url/health

# 2. Verificar Frontend
Abrir en navegador: https://tu-frontend-url

# 3. Verificar API
curl https://tu-backend-url/api/stats
```

## 🛠️ Troubleshooting

### Backend no conecta a Supabase
- Verificar SUPABASE_URL y SUPABASE_KEY en variables de entorno
- Verificar que la base de datos está inicializada
- Revisar logs en Railway/Render

### Frontend no conecta a Backend
- Verificar VITE_API_URL apunta a backend correcto
- Verificar CORS está habilitado en backend (ya está en código)
- Verificar que backend está online

### Errores de Base de Datos
- Supabase tiene límite de 500 MB gratis
- Si datos crecen mucho, upgrade a plan pagado
- O usar Render Database (gratis pero limitado)

## 📊 Límites de Servicios Gratuitos

| Servicio | Límite Gratis | Nota |
|----------|---------------|------|
| Vercel | 100 GB bandwidth/mes | Redeploys ilimitados |
| Railway | 5 GB bandwidth/mes | Suficiente para desarrollo |
| Render | 0.5 GB RAM | Suficiente para MVP |
| Supabase | 500 MB DB | Ampliar si es necesario |

## 📈 Próximos Pasos para Producción

1. Configurar HTTPS (automático en Vercel/Railway)
2. Configurar monitoreo y logging
3. Configurar alertas por email
4. Implementar autenticación si es necesario
5. Mejorar performance
6. Agregar más datos para scoring

---

**¿Problemas?** 
Revisar logs en:
- Railway: Dashboard → Logs
- Vercel: Deployments → Logs
- Supabase: SQL Editor → Errors
