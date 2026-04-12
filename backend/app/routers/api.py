from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.database import db
from app.services.data_ingestion import data_ingestion
from app.services.scoring import scoring_service
from app.schemas import (
    AssetResponse, MarketDataResponse, OpportunityResponse,
    AlertResponse, ScoringResponse, StatsResponse, DashboardSummaryResponse
)
import logging

router = APIRouter(prefix="/api", tags=["assets"])
logger = logging.getLogger(__name__)


# ASSETS ENDPOINTS
@router.get("/assets", response_model=List[AssetResponse])
async def get_all_assets(limit: int = Query(100, ge=1, le=1000)):
    """Get all monitored assets"""
    try:
        assets = await db.get_all_assets(limit=limit)
        return assets
    except Exception as e:
        logger.error(f"Error getting assets: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving assets")


@router.get("/assets/{ticker}", response_model=AssetResponse)
async def get_asset(ticker: str):
    """Get asset by ticker"""
    try:
        asset = await db.get_asset(ticker)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        logger.error(f"Error getting asset: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving asset")


# MARKET DATA ENDPOINTS
@router.get("/market-data/{ticker}", response_model=MarketDataResponse)
async def get_market_data(ticker: str):
    """Get latest market data for ticker"""
    try:
        data = await db.get_latest_market_data(ticker)
        if not data:
            raise HTTPException(status_code=404, detail="Market data not found")
        return data
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        logger.error(f"Error getting market data: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving market data")


@router.get("/market-data/{ticker}/history")
async def get_market_history(ticker: str, days: int = Query(30, ge=1, le=365)):
    """Get market data history"""
    try:
        history = await db.get_market_data_history(ticker, days=days)
        return history
    except Exception as e:
        logger.error(f"Error getting market history: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving market history")


@router.post("/market-data/refresh/{ticker}")
async def refresh_market_data(ticker: str):
    """Fetch and update market data for ticker"""
    try:
        data = await data_ingestion.fetch_and_store_market_data(ticker)
        if not data:
            raise HTTPException(status_code=404, detail="Could not fetch market data")
        return {"status": "success", "data": data}
    except Exception as e:
        logger.error(f"Error refreshing market data: {e}")
        raise HTTPException(status_code=500, detail="Error refreshing market data")


# SCORING ENDPOINTS
@router.get("/scoring/{ticker}", response_model=ScoringResponse)
async def get_scoring(ticker: str):
    """Get latest scoring for ticker"""
    try:
        scoring = await db.get_latest_scoring(ticker)
        if not scoring:
            raise HTTPException(status_code=404, detail="Scoring not found")
        return scoring
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        logger.error(f"Error getting scoring: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving scoring")


@router.post("/scoring/calculate/{ticker}")
async def calculate_scoring(ticker: str):
    """Calculate and save scoring for ticker"""
    try:
        # First fetch latest data
        await data_ingestion.fetch_and_store_market_data(ticker)
        await data_ingestion.fetch_and_store_fundamental_data(ticker)
        
        # Calculate score
        score = await scoring_service.calculate_opportunity_score(ticker)
        
        # Generate recommendation
        recommendation = await scoring_service.generate_opportunity_recommendation(ticker, score)
        
        # If score is high enough, create alert and opportunity
        if score >= 60:
            await db.create_alert(
                ticker=ticker,
                alert_type="new_opportunity",
                message=f"New opportunity detected with score {score:.1f}",
                severity="high" if score >= 75 else "medium"
            )
            
            await db.create_opportunity(
                ticker=ticker,
                reason=recommendation['reason'],
                confidence=recommendation['confidence'],
                entry_price=recommendation['entry_price']
            )
        
        return {
            "status": "success",
            "ticker": ticker,
            "opportunity_score": score,
            "recommendation": recommendation
        }
    except Exception as e:
        logger.error(f"Error calculating scoring: {e}")
        raise HTTPException(status_code=500, detail="Error calculating scoring")


# OPPORTUNITIES ENDPOINTS
@router.get("/opportunities", response_model=List[OpportunityResponse])
async def get_opportunities(limit: int = Query(50, ge=1, le=500)):
    """Get active opportunities"""
    try:
        opportunities = await db.get_active_opportunities(limit=limit)
        return opportunities
    except Exception as e:
        logger.error(f"Error getting opportunities: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving opportunities")


@router.get("/opportunities/top", response_model=List[ScoringResponse])
async def get_top_opportunities(limit: int = Query(10, ge=1, le=100)):
    """Get top opportunities by score"""
    try:
        opportunities = await db.get_top_opportunities(limit=limit)
        return opportunities
    except Exception as e:
        logger.error(f"Error getting top opportunities: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving top opportunities")


# ALERTS ENDPOINTS
@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(limit: int = Query(20, ge=1, le=100), unread_only: bool = False):
    """Get recent alerts"""
    try:
        alerts = await db.get_recent_alerts(limit=limit, unread_only=unread_only)
        return alerts
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving alerts")


@router.post("/alerts/{alert_id}/read")
async def mark_alert_read(alert_id: int):
    """Mark alert as read"""
    try:
        alert = await db.mark_alert_as_read(alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"status": "success", "alert_id": alert_id}
    except Exception as e:
        logger.error(f"Error marking alert as read: {e}")
        raise HTTPException(status_code=500, detail="Error updating alert")


# MONITORING ENDPOINTS
@router.get("/monitoring")
async def get_monitoring():
    """Get monitored assets"""
    try:
        monitored = await db.get_monitored_assets()
        return {"count": len(monitored), "assets": monitored}
    except Exception as e:
        logger.error(f"Error getting monitored assets: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving monitored assets")


@router.post("/monitoring/{ticker}")
async def add_monitoring(ticker: str, asset_type: str = "STOCK"):
    """Add asset to monitoring"""
    try:
        result = await db.add_to_monitoring(ticker, asset_type)
        if not result:
            raise HTTPException(status_code=400, detail="Could not add to monitoring")
        return {"status": "success", "ticker": ticker, "asset_type": asset_type}
    except Exception as e:
        logger.error(f"Error adding to monitoring: {e}")
        raise HTTPException(status_code=500, detail="Error adding to monitoring")


# DASHBOARD ENDPOINTS
@router.get("/dashboard", response_model=DashboardSummaryResponse)
async def get_dashboard_summary():
    """Get dashboard summary with top opportunities and stats"""
    try:
        top_opportunities = await db.get_active_opportunities(limit=10)
        recent_alerts = await db.get_recent_alerts(limit=10)
        monitored = await db.get_monitored_assets()
        all_opportunities = await db.get_active_opportunities(limit=10000)
        
        summary = DashboardSummaryResponse(
            top_opportunities=top_opportunities,
            recent_alerts=recent_alerts,
            monitored_assets_count=len(monitored),
            total_opportunities=len(all_opportunities),
            market_data={}
        )
        return summary
    except Exception as e:
        logger.error(f"Error getting dashboard summary: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving dashboard")


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get general statistics"""
    try:
        assets = await db.get_all_assets(limit=10000)
        opportunities = await db.get_active_opportunities(limit=10000)
        alerts = await db.get_recent_alerts(limit=10000, unread_only=True)
        
        stats = StatsResponse(
            total_assets=len(assets),
            total_opportunities=len(opportunities),
            unread_alerts=len(alerts),
            top_gaining=[],  # Will be populated if we have market data
            top_losing=[]
        )
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving stats")


# SCAN ENDPOINTS
@router.post("/scan/market")
async def scan_market(tickers: List[str] = Query()):
    """Scan multiple tickers for opportunities"""
    try:
        results = []
        for ticker in tickers[:50]:  # Limit to 50 tickers per request
            try:
                score = await scoring_service.calculate_opportunity_score(ticker)
                results.append({"ticker": ticker, "score": score})
            except Exception as e:
                logger.warning(f"Error scanning {ticker}: {e}")
                continue
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return {"status": "success", "results": results}
    except Exception as e:
        logger.error(f"Error scanning market: {e}")
        raise HTTPException(status_code=500, detail="Error scanning market")
