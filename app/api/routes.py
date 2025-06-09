from fastapi import APIRouter, HTTPException
from app.services.data_fetcher import fetch_alpha_vantage_price
from app.crud import insert_forex_price
from app.models.models import ForexPrice

router = APIRouter()

@router.get("/fetch/{base}/{quote}")
async def fetch_and_store_price(base: str, quote: str):
    price = await fetch_alpha_vantage_price(base, quote)
    
    if price is None:
        raise HTTPException(status_code=500, detail="Failed to fetch price from Alpha Vantage")

    await insert_forex_price(base, quote, price, source="AlphaVantage")

    return {
        "base_currency": base,
        "quote_currency": quote,
        "price": price,
        "status": "saved"
    }
