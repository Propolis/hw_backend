from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.users import UserRepository

SECRET_KEY = "secret"
ALGORITM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITM)


async def get_current_user(auth_token: str | None = Header(default=None), db: AsyncSession = Depends(get_db)):
    if not auth_token:
        raise HTTPException(status_code=401, detail="Не авторизован")
    repository = UserRepository(db)
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITM])
        username: str = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    user = await repository.get_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user
