from supabase import create_client, Client
from app.config import settings
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class Database:
    def __init__(self):
        self.client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    
    # ASSETS
    async def create_asset(self, ticker: str, name: str, asset_type: str, sector: str = None, industry: str = None) -> Dict:
        """Create or get asset"""
        try:
            response = self.client.table("assets").upsert(
                {
                    "ticker": ticker,
                    "name": name,
                    "asset_type": asset_type,
                    "sector": sector,
                    "industry": industry,
                    "updated_at": datetime.utcnow().isoformat()
                },
                on_conflict="ticker"
            ).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating asset: {e}")
            return None
    
    async def get_asset(self, ticker: str) -> Dict:
        """Get asset by ticker"""
        try:
            response = self.client.table("assets").select("*").eq("ticker", ticker).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting asset: {e}")
            return None
    
    async def get_all_assets(self, limit: int = 100) -> List[Dict]:
        """Get all assets"""
        try:
            response = self.client.table("assets").select("*").limit(limit).execute()
            return response.data or []
        except Exception as e:
            print(f"Error getting assets: {e}")
            return []
    
    # MARKET DATA
    async def save_market_data(self, ticker: str, price: float, close_price: float, 
                                high_price: float, low_price: float, volume: int, 
                                change_percent: float, market_cap: float = None, 
                                pe_ratio: float = None, dividend_yield: float = None) -> Dict:
        """Save market data"""
        try:
            asset = await self.get_asset(ticker)
            if not asset:
                asset = await self.create_asset(ticker, ticker, "STOCK")
            
            response = self.client.table("market_data").insert({
                "asset_id": asset["id"],
                "ticker": ticker,
                "price": price,
                "close_price": close_price,
                "high_price": high_price,
                "low_price": low_price,
                "volume": volume,
                "change_percent": change_percent,
                "market_cap": market_cap,
                "pe_ratio": pe_ratio,
                "dividend_yield": dividend_yield,
                "date": datetime.utcnow().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving market data: {e}")
            return None
    
    async def get_latest_market_data(self, ticker: str) -> Dict:
        """Get latest market data for ticker"""
        try:
            response = self.client.table("market_data").select("*") \
                .eq("ticker", ticker) \
                .order("date", desc=True) \
                .limit(1) \
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting market data: {e}")
            return None
    
    async def get_market_data_history(self, ticker: str, days: int = 30) -> List[Dict]:
        """Get market data history"""
        try:
            response = self.client.table("market_data").select("*") \
                .eq("ticker", ticker) \
                .order("date", desc=True) \
                .limit(days) \
                .execute()
            return response.data or []
        except Exception as e:
            print(f"Error getting market data history: {e}")
            return []
    
    # FUNDAMENTAL DATA
    async def save_fundamental_data(self, ticker: str, **kwargs) -> Dict:
        """Save fundamental data"""
        try:
            asset = await self.get_asset(ticker)
            if not asset:
                asset = await self.create_asset(ticker, ticker, "STOCK")
            
            data = {
                "asset_id": asset["id"],
                "ticker": ticker,
                "date": datetime.utcnow().isoformat()
            }
            data.update(kwargs)
            
            response = self.client.table("fundamental_data").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving fundamental data: {e}")
            return None
    
    async def get_latest_fundamental_data(self, ticker: str) -> Dict:
        """Get latest fundamental data"""
        try:
            response = self.client.table("fundamental_data").select("*") \
                .eq("ticker", ticker) \
                .order("date", desc=True) \
                .limit(1) \
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting fundamental data: {e}")
            return None
    
    # SCORING
    async def save_scoring(self, ticker: str, fundamental_score: float, valuation_score: float,
                          technical_score: float, news_score: float, risk_score: float,
                          opportunity_score: float) -> Dict:
        """Save scoring"""
        try:
            asset = await self.get_asset(ticker)
            if not asset:
                asset = await self.create_asset(ticker, ticker, "STOCK")
            
            response = self.client.table("scoring").insert({
                "asset_id": asset["id"],
                "ticker": ticker,
                "fundamental_score": fundamental_score,
                "valuation_score": valuation_score,
                "technical_score": technical_score,
                "news_score": news_score,
                "risk_score": risk_score,
                "opportunity_score": opportunity_score,
                "date": datetime.utcnow().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving scoring: {e}")
            return None
    
    async def get_latest_scoring(self, ticker: str) -> Dict:
        """Get latest scoring"""
        try:
            response = self.client.table("scoring").select("*") \
                .eq("ticker", ticker) \
                .order("date", desc=True) \
                .limit(1) \
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting scoring: {e}")
            return None
    
    async def get_top_opportunities(self, limit: int = 10) -> List[Dict]:
        """Get top opportunities by score"""
        try:
            response = self.client.table("scoring").select("*") \
                .order("opportunity_score", desc=True) \
                .limit(limit) \
                .execute()
            return response.data or []
        except Exception as e:
            print(f"Error getting top opportunities: {e}")
            return []
    
    # NEWS
    async def save_news(self, ticker: str, title: str, source: str, url: str,
                       news_type: str, sentiment: str, impact_intensity: int,
                       impact_horizon: str, content: str = None, published_at: str = None) -> Dict:
        """Save news"""
        try:
            asset = await self.get_asset(ticker)
            if not asset:
                asset = await self.create_asset(ticker, ticker, "STOCK")
            
            response = self.client.table("news").insert({
                "asset_id": asset["id"],
                "ticker": ticker,
                "title": title,
                "source": source,
                "url": url,
                "content": content,
                "news_type": news_type,
                "sentiment": sentiment,
                "impact_intensity": impact_intensity,
                "impact_horizon": impact_horizon,
                "published_at": published_at or datetime.utcnow().isoformat()
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error saving news: {e}")
            return None
    
    async def get_recent_news(self, ticker: str = None, limit: int = 20) -> List[Dict]:
        """Get recent news"""
        try:
            query = self.client.table("news").select("*").order("published_at", desc=True)
            if ticker:
                query = query.eq("ticker", ticker)
            response = query.limit(limit).execute()
            return response.data or []
        except Exception as e:
            print(f"Error getting news: {e}")
            return []
    
    # ALERTS
    async def create_alert(self, ticker: str, alert_type: str, message: str, severity: str) -> Dict:
        """Create alert"""
        try:
            asset = await self.get_asset(ticker)
            if not asset:
                asset = await self.create_asset(ticker, ticker, "STOCK")
            
            response = self.client.table("alerts").insert({
                "asset_id": asset["id"],
                "ticker": ticker,
                "alert_type": alert_type,
                "message": message,
                "severity": severity,
                "read": False
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating alert: {e}")
            return None
    
    async def get_recent_alerts(self, limit: int = 20, unread_only: bool = False) -> List[Dict]:
        """Get recent alerts"""
        try:
            query = self.client.table("alerts").select("*").order("created_at", desc=True)
            if unread_only:
                query = query.eq("read", False)
            response = query.limit(limit).execute()
            return response.data or []
        except Exception as e:
            print(f"Error getting alerts: {e}")
            return []
    
    async def mark_alert_as_read(self, alert_id: int) -> Dict:
        """Mark alert as read"""
        try:
            response = self.client.table("alerts").update({"read": True}).eq("id", alert_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error marking alert as read: {e}")
            return None
    
    # OPPORTUNITIES
    async def create_opportunity(self, ticker: str, reason: str, confidence: float,
                                entry_price: float = None, target_price: float = None,
                                stop_loss: float = None) -> Dict:
        """Create opportunity"""
        try:
            asset = await self.get_asset(ticker)
            if not asset:
                asset = await self.create_asset(ticker, ticker, "STOCK")
            
            scoring = await self.get_latest_scoring(ticker)
            
            response = self.client.table("opportunities").insert({
                "asset_id": asset["id"],
                "scoring_id": scoring["id"] if scoring else None,
                "ticker": ticker,
                "reason": reason,
                "confidence": confidence,
                "entry_price": entry_price,
                "target_price": target_price,
                "stop_loss": stop_loss,
                "status": "active"
            }).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating opportunity: {e}")
            return None
    
    async def get_active_opportunities(self, limit: int = 50) -> List[Dict]:
        """Get active opportunities"""
        try:
            response = self.client.table("opportunities").select("*") \
                .eq("status", "active") \
                .order("created_at", desc=True) \
                .limit(limit) \
                .execute()
            return response.data or []
        except Exception as e:
            print(f"Error getting opportunities: {e}")
            return []
    
    async def get_top_opportunities_by_score(self, limit: int = 10) -> List[Dict]:
        """Get top opportunities by confidence"""
        try:
            response = self.client.rpc("get_top_opportunities", {"limit_count": limit}).execute()
            return response.data or []
        except Exception as e:
            print(f"Error getting top opportunities: {e}")
            return []
    
    # MONITORING
    async def add_to_monitoring(self, ticker: str, asset_type: str) -> Dict:
        """Add asset to monitoring"""
        try:
            asset = await self.get_asset(ticker)
            if not asset:
                asset = await self.create_asset(ticker, ticker, asset_type)
            
            response = self.client.table("monitoring").upsert({
                "asset_id": asset["id"],
                "ticker": ticker,
                "asset_type": asset_type,
                "active": True,
                "updated_at": datetime.utcnow().isoformat()
            }, on_conflict="asset_id").execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding to monitoring: {e}")
            return None
    
    async def get_monitored_assets(self) -> List[Dict]:
        """Get all monitored assets"""
        try:
            response = self.client.table("monitoring").select("*").eq("active", True).execute()
            return response.data or []
        except Exception as e:
            print(f"Error getting monitored assets: {e}")
            return []


# Global database instance
db = Database()
