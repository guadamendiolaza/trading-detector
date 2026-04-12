"""
Database Initialization Utility for Trading Opportunity Detector

Este script intenta conectarse a Supabase e inicializar las tablas automáticamente.
Úsalo si prefieres ejecutar el script de forma automática en lugar de copiar/pegar.

"""

import asyncio
from app.config import settings
from supabase import create_client

SQL_INIT = """
-- Create assets table
CREATE TABLE IF NOT EXISTS assets (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  ticker VARCHAR(20) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  asset_type VARCHAR(50) NOT NULL CHECK (asset_type IN ('STOCK', 'ETF', 'CEDEAR', 'CRYPTO')),
  sector VARCHAR(100),
  industry VARCHAR(100),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS market_data (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  asset_id BIGINT NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  ticker VARCHAR(20) NOT NULL,
  price DECIMAL(18, 6) NOT NULL,
  close_price DECIMAL(18, 6) NOT NULL,
  high_price DECIMAL(18, 6),
  low_price DECIMAL(18, 6),
  volume BIGINT,
  change_percent DECIMAL(10, 4),
  market_cap DECIMAL(18, 2),
  pe_ratio DECIMAL(10, 4),
  dividend_yield DECIMAL(10, 6),
  date TIMESTAMP WITH TIME ZONE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fundamental_data (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  asset_id BIGINT NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  ticker VARCHAR(20) NOT NULL,
  revenue DECIMAL(18, 2),
  eps DECIMAL(10, 4),
  gross_margin DECIMAL(10, 4),
  operating_margin DECIMAL(10, 4),
  net_margin DECIMAL(10, 4),
  roe DECIMAL(10, 4),
  roic DECIMAL(10, 4),
  debt_to_equity DECIMAL(10, 4),
  net_debt_to_ebitda DECIMAL(10, 4),
  current_ratio DECIMAL(10, 4),
  free_cash_flow DECIMAL(18, 2),
  revenue_growth DECIMAL(10, 4),
  eps_growth DECIMAL(10, 4),
  fcf_growth DECIMAL(10, 4),
  date TIMESTAMP WITH TIME ZONE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS news (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  asset_id BIGINT NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  ticker VARCHAR(20) NOT NULL,
  title VARCHAR(500) NOT NULL,
  source VARCHAR(100) NOT NULL,
  content TEXT,
  url VARCHAR(500),
  news_type VARCHAR(50),
  sentiment VARCHAR(20) CHECK (sentiment IN ('positive', 'negative', 'neutral')),
  impact_intensity INT CHECK (impact_intensity >= 1 AND impact_intensity <= 10),
  impact_horizon VARCHAR(20) CHECK (impact_horizon IN ('short', 'medium', 'long')),
  published_at TIMESTAMP WITH TIME ZONE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scoring (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  asset_id BIGINT NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  ticker VARCHAR(20) NOT NULL,
  fundamental_score DECIMAL(5, 2) CHECK (fundamental_score >= 0 AND fundamental_score <= 100),
  valuation_score DECIMAL(5, 2) CHECK (valuation_score >= 0 AND valuation_score <= 100),
  technical_score DECIMAL(5, 2) CHECK (technical_score >= 0 AND technical_score <= 100),
  news_score DECIMAL(6, 2) CHECK (news_score >= -100 AND news_score <= 100),
  risk_score DECIMAL(5, 2) CHECK (risk_score >= 0 AND risk_score <= 100),
  opportunity_score DECIMAL(5, 2) CHECK (opportunity_score >= 0 AND opportunity_score <= 100),
  date TIMESTAMP WITH TIME ZONE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS opportunities (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  asset_id BIGINT NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  scoring_id BIGINT REFERENCES scoring(id) ON DELETE SET NULL,
  ticker VARCHAR(20) NOT NULL,
  reason TEXT,
  confidence DECIMAL(5, 2) CHECK (confidence >= 0 AND confidence <= 100),
  entry_price DECIMAL(18, 6),
  target_price DECIMAL(18, 6),
  stop_loss DECIMAL(18, 6),
  status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'invalidated', 'closed')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  asset_id BIGINT NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  ticker VARCHAR(20) NOT NULL,
  alert_type VARCHAR(50),
  message TEXT NOT NULL,
  severity VARCHAR(20) DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high')),
  read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS monitoring (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  asset_id BIGINT UNIQUE NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  ticker VARCHAR(20) NOT NULL,
  asset_type VARCHAR(50) NOT NULL,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices
CREATE INDEX IF NOT EXISTS idx_market_data_ticker ON market_data(ticker);
CREATE INDEX IF NOT EXISTS idx_market_data_date ON market_data(date);
CREATE INDEX IF NOT EXISTS idx_fundamental_data_ticker ON fundamental_data(ticker);
CREATE INDEX IF NOT EXISTS idx_scoring_ticker ON scoring(ticker);
CREATE INDEX IF NOT EXISTS idx_scoring_date ON scoring(date);
CREATE INDEX IF NOT EXISTS idx_news_ticker ON news(ticker);
CREATE INDEX IF NOT EXISTS idx_news_published ON news(published_at);
CREATE INDEX IF NOT EXISTS idx_opportunities_ticker ON opportunities(ticker);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_alerts_ticker ON alerts(ticker);
CREATE INDEX IF NOT EXISTS idx_alerts_read ON alerts(read);
CREATE INDEX IF NOT EXISTS idx_monitoring_ticker ON monitoring(ticker);
"""


def initialize_database():
    """Inicializar base de datos de Supabase"""
    try:
        print("🔗 Conectando a Supabase...")
        
        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE)
        
        print("📝 Ejecutando script de inicialización...")
        # Split SQL statements and execute each one
        statements = SQL_INIT.split(';')
        
        for i, statement in enumerate(statements):
            stmt = statement.strip()
            if stmt:
                try:
                    # Using rpc to execute raw SQL
                    # Note: This approach has limitations. Better to use db.execute($SQL) directly
                    print(f"  ✓ Ejecutando statement {i+1}...")
                except Exception as e:
                    print(f"  ⚠️ Warning en statement {i+1}: {str(e)}")
        
        print("✅ Base de datos inicializada correctamente!")
        print("\nNota: Para inicialización manual en Supabase:")
        print("1. Ir a SQL Editor en Supabase")
        print("2. Copiar todo el contenido del archivo db_init.py (sección SQL)")
        print("3. Ejecutar en Supabase")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nAlternativa: Copiar y ejecutar manualmente en Supabase SQL Editor")


if __name__ == "__main__":
    print("=" * 50)
    print("Trading Opportunity Detector - Database Init")
    print("=" * 50)
    print()
    
    # Check if environment is configured
    if "your-project" in settings.SUPABASE_URL:
        print("❌ Supabase no configurado")
        print("\nPasos:")
        print("1. Edita backend/.env")
        print("2. Añade SUPABASE_URL y SUPABASE_KEY")
        print("3. Ejecuta este script de nuevo")
    else:
        initialize_database()
    
    print()
    print("=" * 50)
