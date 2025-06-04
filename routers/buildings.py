from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import BuildingBase, BuildingOut, FloorBase, FloorOut, RoomBase, RoomOut
from crud import create_building, create_floor, create_room
from models import Room, Floor, Building

router = APIRouter()

@router.get("/", response_model=List[BuildingOut])
def get_buildings(db: Session = Depends(get_db)):
    return db.query(Building).all()

@router.post("/buildings/", response_model=BuildingOut)
async def create_building_endpoint(building: BuildingBase, db: Session = Depends(get_db)):
    return create_building(db, building)

@router.get("/buildings/", response_model=List[BuildingOut])
async def list_buildings(db: Session = Depends(get_db)):
    return db.query(Building).all()

@router.post("/floors/", response_model=FloorOut)
async def create_floor_endpoint(floor: FloorBase, db: Session = Depends(get_db)):
    return create_floor(db, floor)

@router.get("/floors/{building_id}", response_model=List[FloorOut])
async def list_floors(building_id: int, db: Session = Depends(get_db)):
    return db.query(Floor).filter(Floor.building_id == building_id).all()

@router.post("/rooms/", response_model=RoomOut)
async def create_room_endpoint(room: RoomBase, db: Session = Depends(get_db)):
    return create_room(db, room)

@router.get("/rooms/{floor_id}", response_model=List[RoomOut])
async def list_rooms(floor_id: int, db: Session = Depends(get_db)):
    return db.query(Room).filter(Room.floor_id == floor_id).all()