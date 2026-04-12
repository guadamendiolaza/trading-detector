# 🚀 Quick Start Guide

Comienza a usar Trading Opportunity Detector en 5 minutos:

## Opción 1: Desarrollo Local (Recomendado para empezar)

### 1. Preparar Supabase (2 minutos)

1. Ir a https://supabase.com → Sign up (gratis)
2. Create new project
3. En SQL Editor:
   - Crear nueva query
   - Copiar TODO el contenido de `backend/schema.sql`
   - Pegar en el SQL Editor
   - Click en "Run"
4. Anotar credenciales:
   - Project URL (Settings → API)
   - Anon Key (Settings → API)

### 2. Configurar Backend (1 minuto)

```bash
# Windows
cd backend
copy .env.example .env

# macOS/Linux
cd backend
cp .env.example .env
```

Editar `backend/.env`:
```
SUPABASE_URL=tu-url-aqui
SUPABASE_KEY=tu-key-aqui
DEBUG=True
```

### 3. Ejecutar (2 minutos)

**Windows:**
```bash
setup.bat     # Una sola vez para instalar dependencias
run.bat       # Ejecuta backend + frontend
```

**macOS/Linux:**
```bash
bash setup.sh  # Una sola vez para instalar dependencias
bash run.sh    # Ejecuta backend + frontend
```

Esperar a que aparezca:
```
Frontend:  http://localhost:3000
Backend:   http://localhost:8000
```

### 4. Probar

Abrir navegador: http://localhost:3000

¡Listo! Dashboard está corriendo localmente.

---

## Opción 2: Desplegar en Producción (Gratis)

Si quieres que esté disponible online 24/7:

### 1. Crear Repositorio GitHub (3 minutos)

```bash
git init
git add .
git commit -m "Trading Opportunity Detector"
# Crear repo en GitHub y hacer push
```

### 2. Desplegar Backend (5 minutos)

1. Ir a https://railway.app
2. Login con GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Seleccionar tu repo
5. Variables de entorno:
   ```
   SUPABASE_URL=tu-url
   SUPABASE_KEY=tu-key
   DEBUG=False
   ```
6. Deploy

Backend URL: `https://tu-railway-url.railway.app`

### 3. Desplegar Frontend (5 minutos)

1. Ir a https://vercel.com
2. "Add New..." → "Project" → GitHub
3. Seleccionar repo
4. Root Directory: `frontend`
5. Environment variable:
   ```
   VITE_API_URL=https://tu-railway-url.railway.app/api
   ```
6. Deploy

Frontend URL: `https://tu-proyecto.vercel.app`

¡Listo! Aplicación está online gratis.

---

## 📝 Próximas Acciones

### Para Desarrollo Local
- Agregar más activos en "Assets"
- Ejecutar "Refresh Market Data" en cada activo
- Analizar scoring en Dashboard

### Para Producción
- Agregar dominio personalizado (opcional)
- Configurar alertas por email
- Crear usuarios/autenticación
- Agregar más fuentes de datos

---

## ❓ Problemas Comunes

### "No conecta a Supabase"
→ Verificar SUPABASE_URL y SUPABASE_KEY en .env

### "Frontend no ve Backend"
→ En vercel.env, cambiar VITE_API_URL a tu URL de Railway

### "Base de datos no existe"
→ Ejecutar SQL script desde db_init.py en Supabase

### "Error: venv no existe"
→ Ejecutar `setup.bat` (Windows) o `bash setup.sh` (Mac/Linux)

---

## 📚 Documentación Completa

- [README.md](./README.md) - Descripción general
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Guía detallada de despliegue
- [Backend Docs](http://localhost:8000/docs) - API Documentation (Swagger)

---

**¡Que disfrutes usando Trading Opportunity Detector! 🚀📈**
