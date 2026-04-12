from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# Assets
class AssetBase(BaseModel):
    ticker: str
    asset_type: str  # "STOCK", "ETF", "CEDEAR", "CRYPTO"
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Market Data
class MarketDataBase(BaseModel):
    ticker: str
    price: float
    close_price: float
    high_price: float
    low_price: float
    volume: int
    change_percent: float
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None

class MarketDataCreate(MarketDataBase):
    pass

class MarketData(MarketDataBase):
    id: int
    asset_id: int
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# Fundamental Data
class FundamentalDataBase(BaseModel):
    ticker: str
    revenue: Optional[float] = None
    eps: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    roe: Optional[float] = None
    roic: Optional[float] = None
    debt_to_equity: Optional[float] = None
    net_debt_to_ebitda: Optional[float] = None
    current_ratio: Optional[float] = None
    free_cash_flow: Optional[float] = None
    revenue_growth: Optional[float] = None
    eps_growth: Optional[float] = None
    fcf_growth: Optional[float] = None

class FundamentalDataCreate(FundamentalDataBase):
    pass

class FundamentalData(FundamentalDataBase):
    id: int
    asset_id: int
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# News
class NewsBase(BaseModel):
    ticker: str
    title: str
    source: str
    content: Optional[str] = None
    url: str
    news_type: str  # "earnings", "guidance", "demanda", "M&A", etc
    sentiment: str  # "positive", "negative", "neutral"
    impact_intensity: int  # 1-10
    impact_horizon: str  # "short", "medium", "long"

class NewsCreate(NewsBase):
    published_at: datetime

class News(NewsBase):
    id: int
    asset_id: int
    published_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# Scoring
class ScoringBase(BaseModel):
    ticker: str
    fundamental_score: float  # 0-100
    valuation_score: float  # 0-100
    technical_score: float  # 0-100
    news_score: float  # -100 to 100
    risk_score: float  # 0-100
    opportunity_score: float  # final score

class ScoringCreate(ScoringBase):
    pass

class Scoring(ScoringBase):
    id: int
    asset_id: int
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# Opportunity (Resultado)
class OpportunityBase(BaseModel):
    ticker: str
    reason: str
    confidence: float  # 0-100
    entry_price: Optional[float] = None
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None

class OpportunityCreate(OpportunityBase):
    pass

class Opportunity(OpportunityBase):
    id: int
    asset_id: int
    scoring_id: int
    created_at: datetime
    updated_at: datetime
    status: str  # "active", "invalidated", "closed"

    class Config:
        from_attributes = True


# Alert
class AlertBase(BaseModel):
    ticker: str
    alert_type: str  # "new_opportunity", "score_improved", "news_alert", "invalidated"
    message: str
    severity: str  # "low", "medium", "high"

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    asset_id: int
    created_at: datetime
    read: bool = False

    class Config:
        from_attributes = True


# Monitoring
class MonitoringBase(BaseModel):
    ticker: str
    asset_type: str
    active: bool = True

class MonitoringCreate(MonitoringBase):
    pass

class Monitoring(MonitoringBase):
    id: int
    asset_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
