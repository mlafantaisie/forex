from sqlalchemy.future import select
from app.models.users import User
from app.core.database import async_session

async def get_user_by_username(username: str):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()

async def create_user(username: str, password_hash: str):
    async with async_session() as session:
        async with session.begin():
            user = User(username=username, password_hash=password_hash)
            session.add(user)
