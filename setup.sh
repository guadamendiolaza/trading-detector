#!/bin/bash

echo "=========================================="
echo "Trading Opportunity Detector - Setup"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "⚙️  Creando archivo .env..."
    cp backend/.env.example backend/.env
    echo "✓ Archivo .env creado"
    echo "  Por favor, edita backend/.env con tus credenciales de Supabase"
    echo ""
fi

# Create Python virtual environment
echo "🐍 Configurando Python environment..."
cd backend

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

python3 -m venv venv
source venv/bin/activate || . venv/Scripts/activate

echo "✓ Virtual environment creado"

# Install backend dependencies
echo "📦 Instalando dependencias del backend..."
pip install -r requirements.txt
echo "✓ Dependencias del backend instaladas"

cd ..

# Install frontend dependencies
echo "📦 Instalando dependencias del frontend..."
cd frontend
npm install
echo "✓ Dependencias del frontend instaladas"

cd ..

echo ""
echo "=========================================="
echo "✅ Setup completado!"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo "1. Edita backend/.env con tus credenciales de Supabase"
echo "2. Ejecuta el script SQL desde backend/db_init.py en Supabase"
echo "3. Para desarrollar localmente:"
echo "   - Backend: cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo "   - Frontend: cd frontend && npm run dev"
echo ""
echo "O usando Docker Compose:"
echo "   docker-compose up"
echo ""
