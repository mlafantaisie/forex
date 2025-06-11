import httpx
from app.config import settings
from decimal import Decimal

# --- Alpha Vantage ---
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

async def fetch_alpha_vantage_rsi(symbol: str, interval: str = "daily", time_period: int = 14) -> dict:
    params = {
        "function": "RSI",
        "symbol": symbol,
        "interval": interval,
        "time_period": time_period,
        "series_type": "close",
        "apikey": settings.ALPHA_VANTAGE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(ALPHA_VANTAGE_URL, params=params)
        response.raise_for_status()
        data = response.json()

    try:
        print("Alpha Vantage response:", data)
        return data["Technical Analysis: RSI"]
    except Exception as e:
        if "Information" in data:
            print("Alpha Vantage API Limit:", data["Information"])
            return {}
        print("AlphaVantage RSI parsing error:", e)
        return {}


async def fetch_alpha_vantage_price(base: str, quote: str) -> float:
    """
    Fetch single forex price from Alpha Vantage.
    Use cautiously due to strict rate limits (25/day free tier).
    """
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

    try:
        rate_info = data["Realtime Currency Exchange Rate"]
        price = Decimal(rate_info["5. Exchange Rate"])
        return float(price)
    except Exception as e:
        print("AlphaVantage parsing error:", e)
        return None

# --- Finnhub ---
FINNHUB_RATES_URL = "https://finnhub.io/api/v1/forex/rates"
FINNHUB_INDICATOR_URL = "https://finnhub.io/api/v1/indicator"

async def fetch_finnhub_rsi(symbol: str, resolution: str = "D", timeperiod: int = 14) -> dict:
    params = {
        "symbol": symbol,
        "resolution": resolution,
        "indicator": "rsi",
        "timeperiod": timeperiod,
        "token": settings.FINNHUB_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(FINNHUB_INDICATOR_URL, params=params)
        response.raise_for_status()
        data = response.json()

    try:
        rsi_values = data.get("rsi", [])
        timestamps = data.get("t", [])
        if rsi_values and timestamps:
            return {"rsi": round(rsi_values[-1], 2), "timestamp": time.strftime('%Y-%m-%d', time.gmtime(timestamps[-1]))}
    except Exception as e:
        print("Finnhub RSI parsing error:", e)

    return {}

async def fetch_finnhub_quotes(base: str = "USD") -> dict:
    """
    Fetch multiple forex prices from Finnhub.
    Much more API-efficient — allows bulk fetching.
    """
    params = {
        "base": base,
        "token": settings.FINNHUB_API_KEY
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(FINNHUB_RATES_URL, params=params)
        response.raise_for_status()
        data = response.json()

    try:
        return data.get("quote", {})
    except Exception as e:
        print("Finnhub parsing error:", e)
        return {}

async def test_finnhub_connection():
    test_url = "https://finnhub.io/api/v1/quote"
    params = {
        "symbol": "AAPL",
        "token": settings.FINNHUB_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(test_url, params=params)
            print("Status Code:", response.status_code)
            print("Response JSON:", response.json())
        except httpx.HTTPStatusError as e:
            print("HTTP error:", e)
        except Exception as e:
            print("General error:", e)
