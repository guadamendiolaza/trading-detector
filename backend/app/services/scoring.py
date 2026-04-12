import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from app.services.database import db

logger = logging.getLogger(__name__)


class ScoringService:
    """Service for calculating opportunity scores"""
    
    # Scoring weights (as specified in requirements)
    FUNDAMENTAL_WEIGHT = 0.30
    VALUATION_WEIGHT = 0.25
    TECHNICAL_WEIGHT = 0.20
    NEWS_WEIGHT = 0.15
    RISK_WEIGHT = 0.10
    
    def __init__(self):
        pass
    
    async def calculate_fundamental_score(self, fundamental_data: Dict) -> float:
        """
        Calculate fundamental score (0-100)
        Based on: Profitability, Growth, Debt, Cash Flow, Stability
        """
        if not fundamental_data:
            return 50.0  # Default score
        
        scores = []
        
        # 1. Profitability (ROE, margins) - 20 points
        roe = fundamental_data.get('roe', 0)
        if roe:
            roe_score = min(100, (roe / 15.0) * 100)  # 15% ROE = 100
            scores.append(roe_score * 0.2)
        
        net_margin = fundamental_data.get('net_margin', 0)
        if net_margin:
            margin_score = min(100, (net_margin / 0.20) * 100)  # 20% margin = 100
            scores.append(margin_score * 0.2)
        
        # 2. Growth - 20 points
        eps_growth = fundamental_data.get('eps_growth', 0)
        if eps_growth:
            growth_score = min(100, (eps_growth / 0.15) * 100)  # 15% growth = 100
            scores.append(growth_score * 0.2)
        
        revenue_growth = fundamental_data.get('revenue_growth', 0)
        if revenue_growth:
            rev_growth_score = min(100, (revenue_growth / 0.10) * 100)  # 10% growth = 100
            scores.append(rev_growth_score * 0.2)
        
        # 3. Debt and Solvency - 20 points
        debt_to_equity = fundamental_data.get('debt_to_equity', 0)
        if debt_to_equity:
            # Lower debt is better (inverse scoring)
            debt_score = max(0, 100 - (debt_to_equity * 20))  # >5x D/E = 0
            scores.append(debt_score * 0.2)
        
        current_ratio = fundamental_data.get('current_ratio', 0)
        if current_ratio:
            # Optimal is 1.5-3.0
            if current_ratio >= 1.5 and current_ratio <= 3.0:
                liquidity_score = 100
            elif current_ratio >= 1.0:
                liquidity_score = (current_ratio - 0.5) / 2.5 * 100
            else:
                liquidity_score = 0
            scores.append(liquidity_score * 0.2)
        
        # 4. Cash Flow - 20 points
        fcf_growth = fundamental_data.get('fcf_growth', 0)
        if fcf_growth:
            fcf_score = min(100, (fcf_growth / 0.15) * 100)
            scores.append(fcf_score * 0.2)
        
        avg_score = sum(scores) / len(scores) if scores else 50.0
        return min(100, max(0, avg_score))
    
    async def calculate_valuation_score(self, market_data: Dict, fundamental_data: Dict) -> float:
        """
        Calculate valuation score (0-100)
        Based on: P/E ratio, EV/EBITDA, P/B ratio, FCF yield
        """
        if not market_data or not fundamental_data:
            return 50.0
        
        scores = []
        
        # 1. P/E Ratio
        pe_ratio = market_data.get('pe_ratio')
        if pe_ratio and pe_ratio > 0:
            # Lower P/E is better for value investing
            # Historical market average: ~20, Good: <15, Excellent: <10
            if pe_ratio < 10:
                pe_score = 100
            elif pe_ratio < 15:
                pe_score = 80
            elif pe_ratio < 20:
                pe_score = 60
            elif pe_ratio < 30:
                pe_score = 40
            else:
                pe_score = max(0, 100 - (pe_ratio - 30) * 2)
            scores.append(pe_score)
        
        # 2. Price to Book
        price_to_book = market_data.get('price_to_book')
        if price_to_book and price_to_book > 0:
            # Lower P/B is better (value investing)
            if price_to_book < 1.0:
                pb_score = 100
            elif price_to_book < 1.5:
                pb_score = 80
            elif price_to_book < 3.0:
                pb_score = 60
            else:
                pb_score = max(0, 100 - (price_to_book - 3.0) * 10)
            scores.append(pb_score)
        
        # 3. Dividend Yield
        dividend_yield = market_data.get('dividend_yield')
        if dividend_yield:
            # Higher yield is better, but need to check if sustainable
            if dividend_yield > 0.05:
                div_score = min(100, dividend_yield * 500)  # 5%+ = 100
            else:
                div_score = dividend_yield * 2000 if dividend_yield > 0 else 30
            scores.append(div_score)
        
        avg_score = sum(scores) / len(scores) if scores else 50.0
        return min(100, max(0, avg_score))
    
    async def calculate_technical_score(self, market_data: Dict, historical_data: list) -> float:
        """
        Calculate technical/contextual score (0-100)
        Based on: Recent correction, RSI, Volume, Distance to moving average
        """
        if not market_data or not historical_data:
            return 50.0
        
        scores = []
        
        # 1. Recent correction assessment
        price = market_data.get('price', 0)
        if price <= 0:
            return 50.0
        
        # Find highest price in last 52 weeks (approximately 1 year)
        recent_prices = [d.get('close', 0) for d in historical_data[-252:] if d.get('close', 0) > 0]
        
        if recent_prices:
            max_price = max(recent_prices)
            if max_price > 0:
                decline_percent = ((max_price - price) / max_price) * 100
                
                # Score based on decline severity
                if decline_percent < 5:
                    correction_score = 30  # Minimal correction
                elif decline_percent < 15:
                    correction_score = 60  # Moderate correction
                elif decline_percent < 30:
                    correction_score = 80  # Good opportunity
                elif decline_percent < 50:
                    correction_score = 90  # Excellent opportunity
                else:
                    correction_score = max(50, 100 - (decline_percent - 50) / 2)  # Extreme decline
                
                scores.append(correction_score)
        
        # 2. Volume assessment
        volume = market_data.get('volume', 0)
        if volume > 0 and len(historical_data) > 20:
            avg_volume = sum([d.get('volume', 0) for d in historical_data[-20:]]) / 20
            if avg_volume > 0:
                volume_ratio = volume / avg_volume
                if volume_ratio > 2.0:
                    volume_score = 90  # High volume capitulation
                elif volume_ratio > 1.5:
                    volume_score = 75
                elif volume_ratio > 1.0:
                    volume_score = 60
                else:
                    volume_score = 40
                scores.append(volume_score)
        
        avg_score = sum(scores) / len(scores) if scores else 50.0
        return min(100, max(0, avg_score))
    
    async def calculate_news_score(self, news_items: list) -> float:
        """
        Calculate news/sentiment score (-100 to 100)
        Based on sentiment classification and impact intensity
        """
        if not news_items:
            return 0.0
        
        total_score = 0.0
        weights = 0.0
        
        for news in news_items:
            sentiment = news.get('sentiment', 'neutral')
            intensity = news.get('impact_intensity', 5)
            
            # Base sentiment score
            if sentiment == 'positive':
                base_score = 50
            elif sentiment == 'negative':
                base_score = -50
            else:
                base_score = 0
            
            # Adjust by intensity (1-10 scale)
            weighted_score = base_score * (intensity / 5.0)
            
            # Recency weighting (newer news more important)
            # This would need timestamp info
            
            total_score += weighted_score
            weights += 1.0
        
        # Normalize to -100 to 100 range
        avg_score = total_score / weights if weights > 0 else 0
        return max(-100, min(100, avg_score))
    
    async def calculate_risk_score(self, fundamental_data: Dict, market_data: Dict) -> float:
        """
        Calculate risk score (0-100, higher = more risk = lower final score)
        Based on: Debt levels, margin deterioration, volatility
        """
        if not fundamental_data and not market_data:
            return 40.0  # Moderate risk default
        
        risk_level = 0.0
        
        # 1. Debt risk
        debt_to_equity = fundamental_data.get('debt_to_equity', 0)
        if debt_to_equity:
            if debt_to_equity > 3.0:
                risk_level += 40  # High debt risk
            elif debt_to_equity > 2.0:
                risk_level += 25
            elif debt_to_equity > 1.5:
                risk_level += 15
        
        # 2. Margin deterioration risk
        net_margin = fundamental_data.get('net_margin', 0)
        if net_margin and net_margin < 0:
            risk_level += 30  # Negative margins = high risk
        elif net_margin and net_margin < 0.05:
            risk_level += 15  # Low margins
        
        # 3. Current ratio risk
        current_ratio = fundamental_data.get('current_ratio', 0)
        if current_ratio and current_ratio < 1.0:
            risk_level += 20  # Liquidity risk
        
        return min(100, max(0, risk_level))
    
    async def calculate_opportunity_score(self, ticker: str) -> float:
        """
        Calculate final opportunity score
        Formula: 0.30 * fundamental + 0.25 * valuation + 0.20 * technical + 0.15 * news - 0.10 * risk
        """
        try:
            # Get data
            market_data = await db.get_latest_market_data(ticker)
            fundamental_data = await db.get_latest_fundamental_data(ticker)
            historical_data = await db.get_market_data_history(ticker, days=365)
            recent_news = await db.get_recent_news(ticker, limit=20)
            
            if not market_data:
                return 0.0
            
            # Calculate component scores
            fundamental_score = await self.calculate_fundamental_score(fundamental_data)
            valuation_score = await self.calculate_valuation_score(market_data, fundamental_data)
            technical_score = await self.calculate_technical_score(market_data, historical_data)
            news_score = 50 + (await self.calculate_news_score(recent_news) / 2.0)  # Convert to 0-100
            risk_score = await self.calculate_risk_score(fundamental_data, market_data)
            
            # Calculate final opportunity score
            opportunity_score = (
                self.FUNDAMENTAL_WEIGHT * fundamental_score +
                self.VALUATION_WEIGHT * valuation_score +
                self.TECHNICAL_WEIGHT * technical_score +
                self.NEWS_WEIGHT * news_score -
                self.RISK_WEIGHT * risk_score
            )
            
            # Clamp to 0-100
            opportunity_score = max(0, min(100, opportunity_score))
            
            # Save scoring
            await db.save_scoring(
                ticker=ticker,
                fundamental_score=fundamental_score,
                valuation_score=valuation_score,
                technical_score=technical_score,
                news_score=news_score,
                risk_score=risk_score,
                opportunity_score=opportunity_score
            )
            
            return opportunity_score
            
        except Exception as e:
            logger.error(f"Error calculating opportunity score for {ticker}: {e}")
            return 0.0
    
    async def generate_opportunity_recommendation(self, ticker: str, score: float) -> Dict[str, Any]:
        """Generate recommendation based on score"""
        
        market_data = await db.get_latest_market_data(ticker)
        fundamental_data = await db.get_latest_fundamental_data(ticker)
        
        if score >= 75:
            confidence = 90
            reason = "Excellent opportunity: Strong fundamentals, attractive valuation, positive technical setup"
        elif score >= 60:
            confidence = 75
            reason = "Good opportunity: Solid fundamentals with reasonable valuation"
        elif score >= 45:
            confidence = 60
            reason = "Moderate opportunity: Mixed signals, requires monitoring"
        else:
            confidence = 0
            reason = None
        
        return {
            'ticker': ticker,
            'score': score,
            'confidence': confidence,
            'reason': reason,
            'entry_price': market_data.get('price') if market_data else None,
            'current_price': market_data.get('price') if market_data else None
        }


# Global instance
scoring_service = ScoringService()
