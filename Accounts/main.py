from fastapi import FastAPI, HTTPException, Path
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, ForRegister, Users
from schemas import TokenRequest, CreateUser, LoginUser
from other_functions import generate_token, is_token_valid
from datetime import datetime, timedelta

app = FastAPI()

# Jadvalni yaratish
Base.metadata.create_all(bind=engine)

@app.post("/generate-token")
def generate_token_for_user(request: TokenRequest):
    """Foydalanuvchi uchun token generatsiya qilish."""
    db: Session = SessionLocal()
    
    # Tokenni yaratish
    token = generate_token()
    expires_at = datetime.utcnow() + timedelta(minutes=15)  # 15 daqiqa
    
    # Vaqtinchalik accountni yaratish
    temp_account = ForRegister(
        tg_id=request.tg_id,
        phone=request.phone,
        token=token,
        created_at=datetime.utcnow(),
        expires_at=expires_at
    )
    db.add(temp_account)
    db.commit()
    db.refresh(temp_account)
    
    return {"token": token}

@app.get("/cleanup-tokens")
def cleanup_tokens():
    """Muddati o'tgan tokenlarni o'chirish."""
    db: Session = SessionLocal()
    
    # Muddati o'tgan tokenlarni topish va o'chirish
    now = datetime.utcnow()
    expired_tokens = db.query(ForRegister).filter(ForRegister.expires_at < now).all()
    
    for token in expired_tokens:
        db.delete(token)
        
    db.commit()
    
    return {"message": "Token mudati tugagan va o'chirildi!"}

@app.post("/create-user/{token}")
def create_user(token: str, request: CreateUser):
    """Token orqali foydalanuvchi yaratish."""
    db: Session = SessionLocal()
    
    # Tokenni tekshirish
    temp_account = db.query(ForRegister).filter(ForRegister.token == token).first()
    
    if temp_account is None:
        raise HTTPException(status_code=400, detail="Invalid token.")
    
    now = datetime.utcnow()
    if temp_account.expires_at < now:
        # Token muddati o'tgan bo'lsa, uni o'chirish
        db.delete(temp_account)
        db.commit()
        raise HTTPException(status_code=400, detail="Token has expired and has been removed.")
    
    # Foydalanuvchini yaratish
    user = Users(
        tg_id=temp_account.tg_id,
        phone=temp_account.phone,
        full_name=request.full_name,
        sex=request.sex,
        email=request.email,
        username=request.username,
        password=request.password,
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Tokenni o'chirish
    db.delete(temp_account)
    db.commit()
    
    return {"message": "User created successfully."}


# cheack user and random code for login user
@app.post("/login")
def login_user(request: LoginUser):
    pass
