@echo off
echo ==========================================
echo Trading Opportunity Detector - Setup
echo ==========================================
echo.

REM Check if .env exists
if not exist "backend\.env" (
    echo ^o_o Creando archivo .env...
    copy backend\.env.example backend\.env
    echo OK Archivo .env creado
    echo    Por favor, edita backend\.env con tus credenciales de Supabase
    echo.
)

REM Create Python virtual environment
echo ^o_o Configurando Python environment...
cd backend

python -m venv venv
call venv\Scripts\activate.bat

echo OK Virtual environment creado

REM Install backend dependencies
echo ^o_o Instalando dependencias del backend...
pip install -r requirements.txt
echo OK Dependencias del backend instaladas

cd ..

REM Install frontend dependencies
echo ^o_o Instalando dependencias del frontend...
cd frontend
call npm install
echo OK Dependencias del frontend instaladas

cd ..

echo.
echo ==========================================
echo OK Setup completado!
echo ==========================================
echo.
echo Proximos pasos:
echo 1. Edita backend\.env con tus credenciales de Supabase
echo 2. Ejecuta el script SQL desde backend/db_init.py en Supabase
echo 3. Para desarrollar localmente:
echo    - Backend: cd backend ^& venv\Scripts\activate ^& python -m uvicorn app.main:app --reload
echo    - Frontend: cd frontend ^& npm run dev
echo.
pause
