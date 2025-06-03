from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import RoomBase, RoomOut
from crud import create_room
from models import Floor, Room

router = APIRouter(prefix="/rooms", tags=["Помещения"])

@router.post("/", response_model=RoomOut)
async def create_room_endpoint(room: RoomBase, db: Session = Depends(get_db)):
    """Создает новое помещение на указанном этаже."""
    db_floor = db.query(Floor).filter(Floor.id == room.floor_id).first()
    if not db_floor:
        raise HTTPException(status_code=404, detail="Этаж не найден")
    return create_room(db, room)

@router.get("/{floor_id}", response_model=List[RoomOut])
async def list_rooms(floor_id: int, db: Session = Depends(get_db)):
    """Возвращает список всех помещений на указанном этаже."""
    db_floor = db.query(Floor).filter(Floor.id == floor_id).first()
    if not db_floor:
        raise HTTPException(status_code=404, detail="Этаж не найден")
    rooms = db.query(Room).filter(Room.floor_id == floor_id).all()
    return rooms