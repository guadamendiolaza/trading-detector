# 🔧 Supabase Database Setup - Paso a Paso

## ⚠️ IMPORTANTE

Este es un archivo de instrucciones. **NO EJECUTES COMO PYTHON**.

Para inicializar tu base de datos en Supabase, sigue los pasos exactos abajo.

---

## 📋 Pasos para Crear las Tablas

### 1. Crear Proyecto Supabase (si no tienes ya)

```
1. Ir a: https://supabase.com
2. Click "Get Started"
3. Registrarse con GitHub u otro método
4. Click "New Project"
5. Llenar detalles:
   - Project name: trading-detector (o tu nombre)
   - Database Password: (copiar en lugar seguro)
   - Region: (seleccionar cercano a ti)
   - Click "Create New Project"
6. ESPERAR a que se cree (2-3 minutos)
```

### 2. Abrir SQL Editor

```
1. Una vez que el proyecto está creado, ir a:
   Proyecto → SQL Editor (en menu izquierdo)
2. Click en "New Query" (botón azul)
```

### 3. Copiar el SQL

```
1. Abrir archivo: backend/schema.sql (en tu proyecto)
2. COPIAR TODO el contenido (Ctrl+A, Ctrl+C)
```

### 4. Ejecutar en Supabase

```
1. En la pestaña de SQL Editor del navegador
2. PEGAR el contenido (Ctrl+V)
3. Click en el botón azul "Run" en la esquina inferior derecha
4. ESPERAR a que se complete (debe mostrar "Query Executed Successfully")
```

Si ves error, copiar el mensaje y verificar:
- Que todo el SQL fue pegado
- Que no hay caracteres extras
- Que las comillas están correctas

### 5. Verificar que se Crearon las Tablas

```
1. Ir a: Proyecto → Table Editor (menu izquierdo)
2. Deberías ver 8 tablas:
   ✓ assets
   ✓ market_data
   ✓ fundamental_data
   ✓ news
   ✓ scoring
   ✓ opportunities
   ✓ alerts
   ✓ monitoring
3. Si ves todas → ¡Éxito! ✓
```

---

## 🔑 Obtener Credenciales

Una vez verificadas las tablas:

### Paso 1: Ir a Settings

```
1. Proyecto → Settings (engranaje, menu izquierdo)
2. Click en "API"
```

### Paso 2: Copiar las Credenciales

Buscar:
- **Project URL** (debajo de "URLs")
  - Copia esto. Ejemplo: `https://xxxxxxxxxxxxx.supabase.co`
  
- **Anon key** (debajo de "Project API keys")
  - Copia esto. Es una larga cadena de caracteres

### Paso 3: Actualizar tu .env

En tu archivo: `App Trading/backend/.env`

```
SUPABASE_URL=tu-url-copiada-aqui
SUPABASE_KEY=tu-key-copiada-aqui
DEBUG=True
```

Ejemplo:
```
SUPABASE_URL=https://abc123def456ghi789.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J...
DEBUG=True
```

---

## ✅ Verificar Conexión

Para verificar que todo funciona:

```bash
# Windows
setup.bat
run.bat

# Mac/Linux
bash setup.sh
bash run.sh
```

Si ves sin errores:
```
✓ Backend iniciado (PID: ...)
✓ Frontend iniciado (PID: ...)
```

Luego abrir: http://localhost:3000

---

## ❌ Problemas Comunes

### Error: "relation does not exist"
**Causa**: El SQL no se ejecutó correctamente
**Solución**: 
- Volver a SQL Editor
- Borrar query anterior (si es necesario)
- Nueva query
- Pegar SQL nuevamente
- Run

### Error: "duplicate key value violates unique constraint"
**Causa**: Las tablas ya existen
**Solución**:
- Esto es normal si ya ejecutaste el SQL
- Las tablas ya están creadas
- Continúa con el siguiente paso

### "SUPABASE_URL not valid"
**Causa**: URL copiada incorrectamente
**Solución**:
- Ir a Settings → API
- Copiar Project URL nuevamente
- Verificar que empiece con `https://`

### "Backend no conecta"
**Causa**: Key inválida
**Solución**:
- Ir a Settings → API
- Copiar Anon Key nuevamente (la primera en la lista)
- No usar Service Role Key
- Actualizar .env y reiniciar backend

---

## 📞 Soporte

Si tienes problemas:
1. Revisar el error exacto (copiar el mensaje)
2. Verificar que los pasos fueron exactos
3. Intentar nuevamente desde el paso 1

El SQL está validado y funcionará 100% si se copia correctamente.

---

**Última actualización**: Abril 2026
**Archivo SQL**: `backend/schema.sql`
