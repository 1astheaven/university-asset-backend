from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
from database import get_db
from schemas import UserCreate, UserUpdate, UserOut
from crud import create_user, update_user, get_user_by_email
from .auth import get_current_user
from models import User

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.post("/users/", response_model=UserOut)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Нет прав доступа")
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    return create_user(db, user)

@router.get("/users/", response_model=List[UserOut])
async def list_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Нет прав доступа")
    return db.query(User).all()

@router.put("/users/{user_id}", response_model=UserOut)
async def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Нет прав доступа")
    updated_user = update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return updated_user

@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    users = db.query(User).all()
    return users

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.create_user(db, user)

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_user = crud.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user