from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Asset
from schemas import AssetOut, AssetCreate, AssetUpdate  # Убедитесь, что схема определена
from typing import List

router = APIRouter(
    prefix="/assets",
    tags=["assets"]
)

@router.get("/", response_model=List[AssetOut])
def get_assets(room_id: int = None, db: Session = Depends(get_db)):
    try:
        print(f"Запрос активов для room_id: {room_id}")

        query = db.query(Asset)
        if room_id:
            query = query.filter(Asset.room_id == room_id)

        assets = query.all()
        print(f"Найдено активов: {len(assets)}")

        if not assets:
            raise HTTPException(status_code=404, detail="Assets not found")
        return assets
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Ошибка при обработке запроса: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=AssetOut)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    print(f"Создание актива: {asset}")
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.put("/{asset_id}", response_model=AssetOut)
def update_asset(asset_id: int, asset: AssetUpdate, db: Session = Depends(get_db)):
    print(f"Обновление актива с ID: {asset_id}")
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    update_data = asset.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    print(f"Удаление актива с ID: {asset_id}")
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(db_asset)
    db.commit()
    return {"message": "Asset deleted successfully"}