from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="Trading Detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Data
MOCK_OPPORTUNITIES = [
    {"id": 1, "ticker": "AAPL", "confidence": 85.5, "entry": 150, "target": 165, "stop": 145},
    {"id": 2, "ticker": "TSLA", "confidence": 72.3, "entry": 220, "target": 250, "stop": 210},
    {"id": 3, "ticker": "BTC-USD", "confidence": 68.9, "entry": 45000, "target": 52000, "stop": 42000},
    {"id": 4, "ticker": "ETH-USD", "confidence": 62.1, "entry": 2500, "target": 3000, "stop": 2300},
    {"id": 5, "ticker": "MSFT", "confidence": 58.7, "entry": 380, "target": 420, "stop": 365},
]

MOCK_ASSETS = [
    {"id": 1, "ticker": "AAPL", "name": "Apple", "type": "STOCK", "price": 150.25, "change": 2.5},
    {"id": 2, "ticker": "TSLA", "name": "Tesla", "type": "STOCK", "price": 220.75, "change": -1.2},
    {"id": 3, "ticker": "BTC-USD", "name": "Bitcoin", "type": "CRYPTO", "price": 45230.50, "change": 5.3},
]

MOCK_ALERTS = [
    {"id": 1, "message": "AAPL alcanzó resistencia", "severity": "info", "ticker": "AAPL"},
    {"id": 2, "message": "TSLA volumen bajo", "severity": "warning", "ticker": "TSLA"},
    {"id": 3, "message": "BTC rompe soporte", "severity": "danger", "ticker": "BTC-USD"},
]

@app.get("/")
def root():
    return {"message": "Backend Running"}

@app.get("/api/dashboard")
def dashboard():
    return {
        "opportunities": MOCK_OPPORTUNITIES[:5],
        "stats": {
            "total_assets": len(MOCK_ASSETS),
            "opportunities_count": len(MOCK_OPPORTUNITIES),
            "alerts_count": len(MOCK_ALERTS),
            "portfolio_value": 125000.50
        },
        "alerts": MOCK_ALERTS[:3]
    }

@app.get("/api/opportunities")
def opportunities(limit: int = Query(50)):
    return MOCK_OPPORTUNITIES[:limit]

@app.get("/api/opportunities/top")
def top_opportunities(limit: int = Query(10)):
    return MOCK_OPPORTUNITIES[:limit]

@app.get("/api/assets")
def assets(limit: int = Query(100)):
    return MOCK_ASSETS[:limit]

@app.get("/api/assets/{ticker}")
def get_asset(ticker: str):
    for asset in MOCK_ASSETS:
        if asset["ticker"] == ticker:
            return asset
    return {"error": "Asset not found"}

@app.get("/api/alerts")
def alerts(limit: int = Query(20), unread_only: bool = Query(False)):
    return MOCK_ALERTS[:limit]

@app.post("/api/alerts/{alert_id}/read")
def mark_alert_read(alert_id: int):
    return {"success": True}

@app.get("/api/stats")
def stats():
    return {
        "total_assets": len(MOCK_ASSETS),
        "opportunities": len(MOCK_OPPORTUNITIES),
        "alerts": len(MOCK_ALERTS),
        "portfolio": 125000.50,
        "daily_change": 2.5
    }

@app.get("/api/monitoring")
def monitoring():
    return MOCK_ASSETS

@app.post("/api/monitoring/{ticker}")
def add_monitoring(ticker: str, asset_type: str = "STOCK"):
    return {"success": True, "ticker": ticker, "asset_type": asset_type}

@app.get("/api/market-data/{ticker}")
def market_data(ticker: str):
    return {"ticker": ticker, "price": 100.0, "change": 2.5}

@app.get("/api/market-data/{ticker}/history")
def market_history(ticker: str, days: int = 30):
    return {"ticker": ticker, "days": days, "data": []}

@app.post("/api/market-data/refresh/{ticker}")
def refresh_market_data(ticker: str):
    return {"success": True, "ticker": ticker}

@app.get("/api/scoring/{ticker}")
def get_scoring(ticker: str):
    return {"ticker": ticker, "score": 75.5}

@app.post("/api/scoring/calculate/{ticker}")
def calculate_scoring(ticker: str):
    return {"success": True, "ticker": ticker, "score": 75.5}

@app.post("/api/scan/market")
def scan_market(tickers: list = Query([])):
    return {"data": MOCK_OPPORTUNITIES}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
