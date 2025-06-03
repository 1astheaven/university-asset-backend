from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String, nullable=True)
    role = Column(String, default="user")  # пользователь или администратор
    photo = Column(String, nullable=True)

class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    photo = Column(String, nullable=True)

class Floor(Base):
    __tablename__ = "floors"
    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    number = Column(Integer)

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    floor_id = Column(Integer, ForeignKey("floors.id"))
    name = Column(String)

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    photo = Column(String, nullable=True)
    status = Column(String)  # исправно или неисправно
    room_id = Column(Integer, ForeignKey("rooms.id"))
    responsible_user_id = Column(Integer, ForeignKey("users.id"))
    commissioned_date = Column(DateTime, default=datetime.utcnow)
    inventory_number = Column(String, unique=True, index=True)