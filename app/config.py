import os
from dotenv import load_dotenv

# Load .env file if exists
load_dotenv()

class Settings:
    # Alpha Vantage API Key
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")

    # Finnhub API Key
    FINNHUB_API_KEY: str = os.getenv("FINNHUB_API_KEY", "")

    # Other future APIs can be added here

settings = Settings()
