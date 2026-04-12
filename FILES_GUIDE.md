# 📝 Archivos de Configuración - Guía Rápida

Este documento explica qué archivo usar para cada paso.

## 🎯 ¿Cuál archivo necesito?

### Para Inicializar la Base de Datos en Supabase

**USAR: `backend/SQL_COPY_PASTE.txt`**

```
Pasos:
1. Abrir: backend/SQL_COPY_PASTE.txt
2. Copiar TODO el contenido SQL
3. Ir a Supabase SQL Editor
4. New Query
5. Pegar
6. Run
```

⚠️ **NO USES**: `backend/db_init.py` (ese es solo referencia)

---

### Para Entender la Arquitectura

**USAR: `ARCHITECTURE.md`**

- Explicación completa del proyecto
- Diagramas de flujo
- Descripción de componentes
- Schema de base de datos

---

### Para Empezar Rápido (5 minutos)

**USAR: `QUICKSTART.md`**

- Guía paso a paso
- Desarrollo local
- Deployment online

---

### Para Setup Detallado de Supabase

**USAR: `SUPABASE_SETUP.md`**

- Instrucciones paso a paso
- Troubleshooting
- Cómo obtener credenciales
- Qué hacer si hay errores

---

### Para Instalar Dependencias

**USAR: `setup.bat` (Windows) o `setup.sh` (Mac/Linux)**

```bash
Windows:
  setup.bat

Mac/Linux:
  bash setup.sh
```

---

### Para Ejecutar la Aplicación

**USAR: `run.bat` (Windows) o `run.sh` (Mac/Linux)**

```bash
Windows:
  run.bat

Mac/Linux:
  bash run.sh
```

---

### Para Verificar Instalación

**USAR: `verify_installation.py`**

```bash
python verify_installation.py
```

Muestra:
- ✓ Python version OK
- ✓ Node.js installed
- ✓ Dependencies installed
- etc.

---

### Para Desplegar Online (Gratis)

**USAR: `DEPLOYMENT.md`**

- Cómo desplegar en Railway (backend)
- Cómo desplegar en Vercel (frontend)
- Configuración de variables de entorno
- Dominio personalizado

---

## 📂 Estructura de Archivos Clave

```
App Trading/
│
├── QUICKSTART.md               ← LEER PRIMERO (5 min setup)
├── SUPABASE_SETUP.md          ← Instrucciones BD detalladas
├── DEPLOYMENT.md              ← Deploy online gratis
├── ARCHITECTURE.md            ← Documentación técnica
├── README.md                  ← Overview general
│
├── backend/
│   ├── SQL_COPY_PASTE.txt     ← ⭐ Copiar SQL para Supabase
│   ├── schema.sql             ← SQL limpio (alternativa)
│   ├── db_init.py             ← Referencia (no ejecutar)
│   ├── requirements.txt        ← Dependencias Python
│   ├── .env                    ← Configuración (crear)
│   ├── .env.example           ← Template (copiar)
│   └── app/
│       ├── main.py            ← Punto de entrada
│       ├── services/          ← Lógica de negocio
│       ├── routers/           ← Endpoints API
│       └── ...
│
├── frontend/
│   ├── package.json           ← Dependencias Node
│   ├── src/                   ← Código React
│   └── ...
│
├── setup.bat / setup.sh       ← Instalar dependencias
├── run.bat / run.sh           ← Ejecutar app
└── verify_installation.py     ← Verificar instalación

```

---

## 🚀 Flujo de Setup Completo

```
1. LEER: QUICKSTART.md (necesitas saber qué hacer)
   ↓
2. CREAR: Supabase account + proyecto
   ↓
3. USAR: backend/SQL_COPY_PASTE.txt (copiar SQL a Supabase)
   ↓
4. EDITAR: backend/.env (con credenciales)
   ↓
5. EJECUTAR: setup.bat o bash setup.sh
   ↓
6. EJECUTAR: run.bat o bash run.sh
   ↓
7. ABRIR: http://localhost:3000
   ↓
   ✅ ¡Listo!
```

---

## ⚠️ Errores Comunes

### "¿Qué copiar en Supabase?"
→ Usa `backend/SQL_COPY_PASTE.txt`

### "¿Cómo verificar instalación?"
→ Ejecuta `python verify_installation.py`

### "¿Cómo desplegar online?"
→ Lee `DEPLOYMENT.md`

### "¿Backend no conecta a Supabase?"
→ Lee `SUPABASE_SETUP.md` sección "Problemas Comunes"

---

## 📞 Referencia Rápida

| Tarea | Archivo |
|-------|---------|
| **Empezar en 5 min** | QUICKSTART.md |
| **Copiar SQL a Supabase** | backend/SQL_COPY_PASTE.txt |
| **Setup Supabase detallado** | SUPABASE_SETUP.md |
| **Entender arquitectura** | ARCHITECTURE.md |
| **Deploy online** | DEPLOYMENT.md |
| **Instalar dependencias** | setup.bat / setup.sh |
| **Ejecutar app** | run.bat / run.sh |
| **Verificar instalación** | verify_installation.py |

---

## ✅ Checklist de Setup

```
[ ] Leí QUICKSTART.md
[ ] Creé cuenta Supabase
[ ] Copié SQL desde SQL_COPY_PASTE.txt
[ ] Ejecuté SQL en Supabase SQL Editor
[ ] Copié credenciales a backend/.env
[ ] Ejecuté setup.bat / setup.sh
[ ] Ejecuté run.bat / run.sh
[ ] Abrí http://localhost:3000
[ ] ¡Veo el dashboard!
```

---

¡Éxito con tu setup! 🚀

Última actualización: Abril 2026
