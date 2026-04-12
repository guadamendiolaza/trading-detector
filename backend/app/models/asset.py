from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# Asset
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
