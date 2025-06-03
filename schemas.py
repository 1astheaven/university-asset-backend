from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    role: str = "user"

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    photo: Optional[str] = None

class UserOut(UserBase):
    id: int
    photo: Optional[str] = None
    class Config:
        orm_mode = True

class BuildingBase(BaseModel):
    name: str
    address: str
    photo: Optional[str] = None

class BuildingOut(BuildingBase):
    id: int
    class Config:
        orm_mode = True

class FloorBase(BaseModel):
    building_id: int
    number: int

class FloorOut(FloorBase):
    id: int
    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    floor_id: int
    name: str

class RoomOut(RoomBase):
    id: int
    class Config:
        orm_mode = True

class AssetBase(BaseModel):
    name: str
    category: str
    status: str
    room_id: int
    responsible_user_id: int
    inventory_number: str
    photo: Optional[str] = None

class AssetCreate(AssetBase):
    commissioned_date: Optional[datetime] = None

class AssetOut(AssetBase):
    id: int
    commissioned_date: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str