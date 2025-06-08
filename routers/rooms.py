from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Room
from schemas import RoomOut
from typing import List

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"]
)

@router.get("/", response_model=List[RoomOut])
def get_rooms(floor_id: int = None, db: Session = Depends(get_db)):
    try:
        print(f"Запрос комнат для floor_id: {floor_id}")

        query = db.query(Room)
        if floor_id:
            query = query.filter(Room.floor_id == floor_id)

        rooms = query.all()
        print(f"Найдено комнат: {len(rooms)}")

        if not rooms:
            raise HTTPException(status_code=404, detail="Rooms not found")
        return rooms
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"Ошибка при обработке запроса: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")