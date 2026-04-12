-- Trading Opportunity Detector - Database Initialization
-- Copy and paste ALL of this into Supabase SQL Editor and click "Run"

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

-- Create market_data table
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

-- Create fundamental_data table
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

-- Create news table
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

-- Create scoring table
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

-- Create opportunities table
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

-- Create alerts table
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

-- Create monitoring table
CREATE TABLE IF NOT EXISTS monitoring (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  asset_id BIGINT UNIQUE NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
  ticker VARCHAR(20) NOT NULL,
  asset_type VARCHAR(50) NOT NULL,
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
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

-- Create function to get top opportunities
CREATE OR REPLACE FUNCTION get_top_opportunities(limit_count INT DEFAULT 10)
RETURNS TABLE (
  id BIGINT,
  ticker VARCHAR,
  reason TEXT,
  confidence DECIMAL,
  entry_price DECIMAL,
  target_price DECIMAL,
  stop_loss DECIMAL,
  status VARCHAR,
  created_at TIMESTAMP WITH TIME ZONE,
  updated_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    o.id, o.ticker, o.reason, o.confidence, o.entry_price,
    o.target_price, o.stop_loss, o.status, o.created_at, o.updated_at
  FROM opportunities o
  WHERE o.status = 'active'
  ORDER BY o.confidence DESC, o.created_at DESC
  LIMIT limit_count;
END;
$$ LANGUAGE plpgsql;
