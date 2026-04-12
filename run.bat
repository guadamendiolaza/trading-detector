@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo Trading Opportunity Detector - Dev Run
echo ==========================================
echo.

REM Check .env exists
if not exist "backend\.env" (
    echo xx backend\.env no existe
    echo    Ejecuta: copy backend\.env.example backend\.env
    echo    Y configura tus credenciales de Supabase
    pause
    exit /b 1
)

REM Check virtual environment
if not exist "backend\venv" (
    echo xx Virtual environment no existe
    echo    Ejecuta: python -m venv backend\venv
    echo    O ejecuta: setup.bat
    pause
    exit /b 1
)

REM Check node_modules
if not exist "frontend\node_modules" (
    echo xx node_modules no existe
    echo    Ejecuta: cd frontend ^& npm install
    echo    O ejecuta: setup.bat
    pause
    exit /b 1
)

echo OK Configuracion verificada
echo.

echo o_o Iniciando Backend...
cd backend
call venv\Scripts\activate.bat
start /b python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
cd ..
timeout /t 2 /nobreak
echo OK Backend iniciado
echo.

echo o_o Iniciando Frontend...
cd frontend
start /b npm run dev
cd ..
timeout /t 2 /nobreak
echo OK Frontend iniciado
echo.

echo ==========================================
echo OK Aplicacion ejecutandose
echo ==========================================
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:8000
echo Docs API:  http://localhost:8000/docs
echo.
echo Para detener: Cierra las ventanas o presiona Ctrl+C
echo.
pause
