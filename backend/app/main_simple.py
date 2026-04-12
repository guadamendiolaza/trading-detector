from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Trading Opportunity Detector")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Asset(BaseModel):
    id: int
    ticker: str
    name: str
    asset_type: str
    price: float
    change_percent: float

class Opportunity(BaseModel):
    id: int
    ticker: str
    confidence: float
    entry_price: float
    target_price: float
    stop_loss: float

class Alert(BaseModel):
    id: int
    message: str
    severity: str
    created_at: str

# Mock Data
MOCK_OPPORTUNITIES = [
    Opportunity(id=1, ticker="AAPL", confidence=85.5, entry_price=150.0, target_price=165.0, stop_loss=145.0),
    Opportunity(id=2, ticker="TSLA", confidence=72.3, entry_price=220.0, target_price=250.0, stop_loss=210.0),
    Opportunity(id=3, ticker="BTC-USD", confidence=68.9, entry_price=45000.0, target_price=52000.0, stop_loss=42000.0),
]

MOCK_ASSETS = [
    Asset(id=1, ticker="AAPL", name="Apple Inc.", asset_type="stock", price=150.25, change_percent=2.5),
    Asset(id=2, ticker="TSLA", name="Tesla Inc.", asset_type="stock", price=220.75, change_percent=-1.2),
    Asset(id=3, ticker="BTC-USD", name="Bitcoin", asset_type="crypto", price=45230.50, change_percent=5.3),
]

MOCK_ALERTS = [
    Alert(id=1, message="AAPL alcanzó resistencia clave", severity="info", created_at=datetime.now().isoformat()),
    Alert(id=2, message="TSLA volumen bajó significativamente", severity="warning", created_at=datetime.now().isoformat()),
]

# Routes
@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Trading Backend Running"}

@app.get("/api/opportunities")
def get_opportunities() -> List[Opportunity]:
    return MOCK_OPPORTUNITIES

@app.get("/api/assets")
def get_assets() -> List[Asset]:
    return MOCK_ASSETS

@app.get("/api/alerts")
def get_alerts() -> List[Alert]:
    return MOCK_ALERTS

@app.get("/api/dashboard")
def get_dashboard():
    return {
        "opportunities": MOCK_OPPORTUNITIES,
        "assets": MOCK_ASSETS,
        "alerts": MOCK_ALERTS,
        "stats": {
            "total_assets": len(MOCK_ASSETS),
            "active_opportunities": len(MOCK_OPPORTUNITIES),
            "pending_alerts": len(MOCK_ALERTS),
            "portfolio_value": 125000.50,
            "daily_change": 2.5
        }
    }

@app.post("/api/assets")
def add_asset(asset: Asset):
    return {"success": True, "message": "Asset added", "asset": asset}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
