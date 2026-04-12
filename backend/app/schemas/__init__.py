from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# Asset Schema
class AssetResponse(BaseModel):
    id: int
    ticker: str
    name: str
    asset_type: str
    sector: Optional[str]
    industry: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Market Data Schema
class MarketDataResponse(BaseModel):
    id: int
    ticker: str
    price: float
    close_price: float
    high_price: float
    low_price: float
    volume: int
    change_percent: float
    market_cap: Optional[float]
    pe_ratio: Optional[float]
    dividend_yield: Optional[float]
    date: datetime

    class Config:
        from_attributes = True


# Fundamental Data Schema
class FundamentalDataResponse(BaseModel):
    id: int
    ticker: str
    revenue: Optional[float]
    eps: Optional[float]
    gross_margin: Optional[float]
    operating_margin: Optional[float]
    net_margin: Optional[float]
    roe: Optional[float]
    roic: Optional[float]
    debt_to_equity: Optional[float]
    net_debt_to_ebitda: Optional[float]
    current_ratio: Optional[float]
    free_cash_flow: Optional[float]
    revenue_growth: Optional[float]
    eps_growth: Optional[float]
    date: datetime

    class Config:
        from_attributes = True


# News Schema
class NewsResponse(BaseModel):
    id: int
    ticker: str
    title: str
    source: str
    content: Optional[str]
    url: str
    news_type: str
    sentiment: str
    impact_intensity: int
    impact_horizon: str
    published_at: datetime

    class Config:
        from_attributes = True


# Scoring Schema
class ScoringResponse(BaseModel):
    id: int
    ticker: str
    fundamental_score: float
    valuation_score: float
    technical_score: float
    news_score: float
    risk_score: float
    opportunity_score: float
    date: datetime

    class Config:
        from_attributes = True


# Opportunity Schema
class OpportunityResponse(BaseModel):
    id: int
    ticker: str
    reason: str
    confidence: float
    entry_price: Optional[float]
    target_price: Optional[float]
    stop_loss: Optional[float]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Alert Schema
class AlertResponse(BaseModel):
    id: int
    ticker: str
    alert_type: str
    message: str
    severity: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Dashboard Summary
class DashboardSummaryResponse(BaseModel):
    top_opportunities: List[OpportunityResponse]
    recent_alerts: List[AlertResponse]
    monitored_assets_count: int
    total_opportunities: int
    market_data: Optional[dict]

    class Config:
        from_attributes = True


# Stats Schema
class StatsResponse(BaseModel):
    total_assets: int
    total_opportunities: int
    unread_alerts: int
    top_gaining: List[MarketDataResponse]
    top_losing: List[MarketDataResponse]

    class Config:
        from_attributes = True
