from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class ForexPrice(Base):
    __tablename__ = "forex_prices"

    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String(10), nullable=False)
    quote_currency = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    source = Column(String(50), nullable=False)  # e.g. "AlphaVantage" or "Finnhub"
