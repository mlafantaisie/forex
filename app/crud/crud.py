from sqlalchemy.future import select
from sqlalchemy import desc
from app.models.models import ForexPrice
from app.core.database import async_session

# Insert new price record
async def insert_forex_price(base: str, quote: str, price: float, source: str):
    async with async_session() as session:
        async with session.begin():
            record = ForexPrice(
                base_currency=base,
                quote_currency=quote,
                price=price,
                source=source
            )
            session.add(record)

# Get recent prices for a currency pair
async def get_recent_prices(base: str, quote: str, limit: int = 100):
    async with async_session() as session:
        result = await session.execute(
            select(ForexPrice)
            .where(ForexPrice.base_currency == base)
            .where(ForexPrice.quote_currency == quote)
            .order_by(desc(ForexPrice.timestamp))
            .limit(limit)
        )
        return result.scalars().all()
