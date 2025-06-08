from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    role: str = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    password: str  # Добавьте это поле
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "user"

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True

class BuildingBase(BaseModel):
    name: str
    address: str
    photo: Optional[str] = None

class BuildingOut(BuildingBase):
    id: int
    class Config:
        from_attributes = True

class FloorBase(BaseModel):
    building_id: int
    number: int

class FloorOut(FloorBase):
    id: int
    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    floor_id: int
    name: str

class RoomOut(RoomBase):
    id: int
    class Config:
        from_attributes = True

class AssetBase(BaseModel):
    name: str
    category: str
    status: str
    room_id: int
    responsible_user_id: int
    inventory_number: str
    photo: Optional[str] = None

class AssetCreate(BaseModel):
    name: str
    category: str
    status: str
    room_id: int
    responsible_user_id: int
    inventory_number: str
    photo: Optional[str] = None
    commissioned_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    room_id: Optional[int] = None
    responsible_user_id: Optional[int] = None
    inventory_number: Optional[str] = None
    photo: Optional[str] = None
    commissioned_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class AssetOut(BaseModel):
    id: int
    name: str
    category: str
    status: str
    room_id: int
    responsible_user_id: int
    inventory_number: str
    photo: Optional[str] = None
    commissioned_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
