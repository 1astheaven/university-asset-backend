from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import AssetCreate, AssetOut
from crud import create_asset, generate_qr_code
from auth import get_current_user
from PIL import Image
import io

router = APIRouter()

@router.post("/assets/", response_model=AssetOut)
async def create_asset_endpoint(asset: AssetCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Нет прав доступа")
    return create_asset(db, asset)

@router.get("/assets/room/{room_id}", response_model=List[AssetOut])
async def list_assets(room_id: int, db: Session = Depends(get_db)):
    return db.query(Asset).filter(Asset.room_id == room_id).all()

@router.get("/assets/{inventory_number}", response_model=AssetOut)
async def get_asset(inventory_number: str, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.inventory_number == inventory_number).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Имущество не найдено")
    return asset

@router.post("/assets/upload-photo/")
async def upload_asset_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Заглушка для распознавания изображения (не реализовано)
    image = Image.open(io.BytesIO(await file.read()))
    # Симуляция распознавания
    name = "Распознанный предмет"  # Замените на вывод реальной ML-модели
    category = "Неизвестно"        # Замените на вывод реальной ML-модели
    return {"name": name, "category": category}

@router.get("/assets/qr/{inventory_number}")
async def get_qr_code(inventory_number: str, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.inventory_number == inventory_number).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Имущество не найдено")
    qr_code = generate_qr_code(inventory_number)
    return {"qr_code": f"data:image/png;base64,{qr_code}"}