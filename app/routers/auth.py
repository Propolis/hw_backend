from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserLogin, Token
from app.database import get_db
from app.repositories.users import UserRepository
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    if repository.get_by_username(user.username):
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    repository.create(user.username, user.email, hash_password(user.password))
    return {"detail": "Зарегистрирован"}


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    repository = UserRepository(db)
    db_user = repository.get_by_username(user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные учётные данные")
    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
