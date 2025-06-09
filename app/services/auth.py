import bcrypt
from passlib.context import CryptContext
from itsdangerous import URLSafeSerializer
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

serializer = URLSafeSerializer("SECRET_KEY_CHANGE_ME")

def create_session_token(username: str):
    return serializer.dumps({"user": username})

def verify_session_token(token: str):
    try:
        data = serializer.loads(token)
        return data["user"]
    except Exception:
        return None
