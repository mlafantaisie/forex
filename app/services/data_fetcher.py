import httpx
from app.core.config import settings
from decimal import Decimal

# Alpha Vantage base URL
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

async def fetch_alpha_vantage_price(base: str, quote: str) -> float:
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": base,
        "to_currency": quote,
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(ALPHA_VANTAGE_URL, params=params)
        response.raise_for_status()
        data = response.json()

    # Parse result safely
    try:
        rate_info = data["Realtime Currency Exchange Rate"]
        price = Decimal(rate_info["5. Exchange Rate"])
        return float(price)
    except Exception as e:
        print("Error parsing Alpha Vantage response:", e)
        return None
