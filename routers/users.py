from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import UserCreate, UserUpdate, UserOut
from crud import create_user, update_user, get_user_by_email
from auth import get_current_user

router = APIRouter()

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