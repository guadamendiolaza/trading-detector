import yfinance as yf
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from app.services.database import db

logger = logging.getLogger(__name__)


class DataIngestionService:
    """Service for fetching market data from various sources"""
    
    def __init__(self):
        self.yfinance_client = yf
    
    async def fetch_stock_data(self, ticker: str) -> Dict[str, Any]:
        """Fetch stock data from yfinance"""
        try:
            stock = yf.Ticker(ticker)
            
            # Get current data
            hist = stock.history(period="1d")
            if hist.empty:
                return None
            
            current_row = hist.iloc[-1]
            price = current_row['Close']
            high = current_row['High']
            low = current_row['Low']
            volume = int(current_row['Volume'])
            
            # Get info
            info = stock.info
            market_cap = info.get('marketCap')
            pe_ratio = info.get('trailingPE')
            dividend_yield = info.get('dividendYield')
            previous_close = info.get('previousClose', price)
            
            change_percent = ((price - previous_close) / previous_close * 100) if previous_close else 0
            
            return {
                'ticker': ticker,
                'price': float(price),
                'close_price': float(price),
                'high_price': float(high),
                'low_price': float(low),
                'volume': volume,
                'change_percent': float(change_percent),
                'market_cap': float(market_cap) if market_cap else None,
                'pe_ratio': float(pe_ratio) if pe_ratio else None,
                'dividend_yield': float(dividend_yield) if dividend_yield else None,
                'name': info.get('longName', ticker),
                'sector': info.get('sector'),
                'industry': info.get('industry')
            }
        except Exception as e:
            logger.error(f"Error fetching stock data for {ticker}: {e}")
            return None
    
    async def fetch_fundamental_data(self, ticker: str) -> Dict[str, Any]:
        """Fetch fundamental data from yfinance"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            quarterly_financials = stock.quarterly_financials
            
            # Extract fundamental metrics
            data = {
                'ticker': ticker,
                'revenue': info.get('totalRevenue'),
                'eps': info.get('trailingEps'),
                'gross_margin': info.get('grossMargins'),
                'operating_margin': info.get('operatingMargins'),
                'net_margin': info.get('profitMargins'),
                'roe': info.get('returnOnEquity'),
                'roic': info.get('returnOnCapital') if hasattr(info, 'returnOnCapital') else None,
                'debt_to_equity': info.get('debtToEquity'),
                'net_debt_to_ebitda': None,  # Not directly available in yfinance
                'current_ratio': info.get('currentRatio'),
                'free_cash_flow': info.get('freeCashflow'),
                'revenue_growth': None,
                'eps_growth': None,
                'fcf_growth': None
            }
            
            # Clean up None values
            return {k: v for k, v in data.items() if v is not None}
        except Exception as e:
            logger.error(f"Error fetching fundamental data for {ticker}: {e}")
            return None
    
    async def fetch_historical_prices(self, ticker: str, period: str = "3mo") -> List[Dict]:
        """Fetch historical price data"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            data_list = []
            for date, row in hist.iterrows():
                data_list.append({
                    'ticker': ticker,
                    'date': date.isoformat(),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume']),
                    'change_percent': None  # Will be calculated
                })
            
            return data_list
        except Exception as e:
            logger.error(f"Error fetching historical prices for {ticker}: {e}")
            return []
    
    async def fetch_news(self, ticker: str, source: str = "newsapi") -> List[Dict]:
        """Fetch news for a ticker"""
        try:
            if source == "newsapi":
                return await self._fetch_from_newsapi(ticker)
            else:
                return []
        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {e}")
            return []
    
    async def _fetch_from_newsapi(self, ticker: str) -> List[Dict]:
        """Fetch from NewsAPI"""
        try:
            # This would require NewsAPI key in config
            # For now, returning empty list
            return []
        except Exception as e:
            logger.error(f"Error with NewsAPI: {e}")
            return []
    
    async def fetch_etf_data(self, ticker: str) -> Dict[str, Any]:
        """Fetch ETF data"""
        return await self.fetch_stock_data(ticker)
    
    async def fetch_cedear_data(self, ticker: str) -> Dict[str, Any]:
        """Fetch CEDEAR data (Argentine ADRs)"""
        return await self.fetch_stock_data(ticker)
    
    async def fetch_crypto_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch cryptocurrency data"""
        try:
            # Try to fetch from yfinance with -USD suffix
            ticker = f"{symbol.upper()}-USD"
            stock = yf.Ticker(ticker)
            
            hist = stock.history(period="1d")
            if hist.empty:
                return None
            
            current_row = hist.iloc[-1]
            price = current_row['Close']
            previous_close = price * 1.01  # Approximate if not available
            change_percent = -1  # Placeholder
            
            return {
                'ticker': symbol.upper(),
                'price': float(price),
                'close_price': float(price),
                'high_price': float(current_row['High']),
                'low_price': float(current_row['Low']),
                'volume': int(current_row['Volume']),
                'change_percent': float(change_percent),
                'market_cap': None,
                'name': symbol.upper(),
                'asset_type': 'CRYPTO'
            }
        except Exception as e:
            logger.error(f"Error fetching crypto data for {symbol}: {e}")
            return None
    
    async def fetch_and_store_market_data(self, ticker: str, asset_type: str = "STOCK"):
        """Fetch and store market data"""
        try:
            if asset_type == "CRYPTO":
                data = await self.fetch_crypto_data(ticker)
            elif asset_type == "ETF":
                data = await self.fetch_etf_data(ticker)
            elif asset_type == "CEDEAR":
                data = await self.fetch_cedear_data(ticker)
            else:
                data = await self.fetch_stock_data(ticker)
            
            if data:
                await db.save_market_data(
                    ticker=data['ticker'],
                    price=data.get('price'),
                    close_price=data.get('close_price'),
                    high_price=data.get('high_price'),
                    low_price=data.get('low_price'),
                    volume=data.get('volume', 0),
                    change_percent=data.get('change_percent', 0),
                    market_cap=data.get('market_cap'),
                    pe_ratio=data.get('pe_ratio'),
                    dividend_yield=data.get('dividend_yield')
                )
                return data
        except Exception as e:
            logger.error(f"Error fetching and storing market data for {ticker}: {e}")
        
        return None
    
    async def fetch_and_store_fundamental_data(self, ticker: str):
        """Fetch and store fundamental data"""
        try:
            data = await self.fetch_fundamental_data(ticker)
            if data:
                await db.save_fundamental_data(ticker, **data)
                return data
        except Exception as e:
            logger.error(f"Error fetching and storing fundamental data for {ticker}: {e}")
        
        return None


# Global instance
data_ingestion = DataIngestionService()
