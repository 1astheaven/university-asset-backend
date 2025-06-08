from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import UserCreate, UserUpdate, UserOut
from crud import create_user, update_user, get_user_by_email
from .auth import get_current_user, get_password_hash
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
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        # Проверка уникальности email
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = get_password_hash(user.password)
        new_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        print(f"Ошибка при создании пользователя: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":  # Изменено с .get("role") на .role
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        print(f"Обновляем пользователя {user_id} с данными: {user.dict(exclude_unset=True)}")
        update_data = user.dict(exclude_unset=True, exclude={"password"})
        if user.password:
            update_data["hashed_password"] = get_password_hash(user.password)
        for key, value in update_data.items():
            print(f"Устанавливаем {key} = {value}")
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Ошибка при обновлении пользователя: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")