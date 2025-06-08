from sqlalchemy.orm import Session
from models import User, Building, Floor, Room, Asset
from schemas import UserCreate, UserUpdate, AssetCreate, BuildingBase, FloorBase, RoomBase
import bcrypt
import qrcode
import io
import base64

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    if user.password and user.password != user.confirm_password:
        raise ValueError("Пароли не совпадают")
    for key, value in user.dict(exclude_unset=True).items():
        if key not in ["password", "confirm_password"]:
            setattr(db_user, key, value)
    if user.password:
        db_user.hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    db.commit()
    db.refresh(db_user)
    return db_user

def create_building(db: Session, building: BuildingBase):
    db_building = Building(**building.dict())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building

def create_floor(db: Session, floor: FloorBase):
    db_floor = Floor(**floor.dict())
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)
    return db_floor

def create_room(db: Session, room: RoomBase):
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def create_asset(db: Session, asset: AssetCreate):
    db_asset = Asset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def generate_qr_code(inventory_number: str):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(inventory_number)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()