from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

metadata = sqlalchemy.MetaData()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    echo=True  # Set True for SQL debug logs
)

# Session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()
