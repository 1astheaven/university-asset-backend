from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Floor  # Модель этажа
from schemas import FloorOut  # Схема вывода (если определена)
from typing import List

# Создание маршрутизатора с префиксом и тегами
router = APIRouter(
    prefix="/floors",
    tags=["floors"]
)

# Эндпоинт для получения списка этажей
@router.get("/", response_model=List[FloorOut])
def get_floors(building_id: int = None, db: Session = Depends(get_db)):
    try:
        # Логирование для отладки
        print(f"Запрос этажей для building_id: {building_id}")

        # Формирование запроса
        query = db.query(Floor)
        if building_id:
            query = query.filter(Floor.building_id == building_id)

        # Получение данных
        floors = query.all()
        print(f"Найдено этажей: {len(floors)}")

        if not floors:
            raise HTTPException(status_code=404, detail="Floors not found")

        return floors
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Ошибка при обработке запроса: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# (Опционально) Эндпоинт для получения одного этажа по ID
@router.get("/{floor_id}", response_model=FloorOut)
def get_floor(floor_id: int, db: Session = Depends(get_db)):
    try:
        print(f"Запрос этажа с ID: {floor_id}")
        floor = db.query(Floor).filter(Floor.id == floor_id).first()
        if not floor:
            raise HTTPException(status_code=404, detail="Floor not found")
        return floor
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Ошибка при обработке запроса: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")