#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Trading Opportunity Detector - Dev Run${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check .env exists
if [ ! -f backend/.env ]; then
    echo "❌ backend/.env no existe"
    echo "   Ejecuta: cp backend/.env.example backend/.env"
    echo "   Y configura tus credenciales de Supabase"
    exit 1
fi

# Check virtual environment
if [ ! -d "backend/venv" ]; then
    echo "❌ Virtual environment no existe"
    echo "   Ejecuta: python -m venv backend/venv"
    echo "   O ejecuta: bash setup.sh"
    exit 1
fi

# Check node_modules
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ node_modules no existe"
    echo "   Ejecuta: cd frontend && npm install"
    echo "   O ejecuta: bash setup.sh"
    exit 1
fi

echo -e "${GREEN}✓ Configuración verificada${NC}"
echo ""

# Start backend in background
echo -e "${BLUE}🚀 Iniciando Backend...${NC}"
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..
sleep 2
echo -e "${GREEN}✓ Backend iniciado (PID: $BACKEND_PID)${NC}"
echo ""

# Start frontend in background
echo -e "${BLUE}🚀 Iniciando Frontend...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..
sleep 2
echo -e "${GREEN}✓ Frontend iniciado (PID: $FRONTEND_PID)${NC}"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Aplicación ejecutándose${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:8000"
echo "Docs API:  http://localhost:8000/docs"
echo ""
echo "Para detener: Presiona Ctrl+C"
echo ""

# Trap to clean up both processes on exit
cleanup() {
    echo ""
    echo -e "${BLUE}Deteniendo servicios...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID 2>/dev/null
    wait $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✓ Servicios detenidos${NC}"
    exit 0
}

trap cleanup EXIT INT TERM

# Wait indefinitely
wait
