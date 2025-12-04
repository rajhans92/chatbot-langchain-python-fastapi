from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.helpers.database import get_db
from app.schemas.usersSchemas import UserCreate, UserLogin
from app.models.usersModels import Users
from app.helpers.hashing import hash_password, verify_password
from app.helpers.jwt import create_jwt_token


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    userExist = db.query(Users).filter(Users.email == user.email).first()
    if userExist:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(user.password)
    new_user = Users(name=user.name, email=user.email, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    jwt_token = create_jwt_token({"user_id":db_user.id, "user_name": db_user.name, "user_email":db_user.email})

    return {"message": "User logged in successfully", "token":jwt_token, "user_name": db_user.name, "user_email":db_user.email}

@router.post("/profile")
def get_user_profile():
    return {"message": "User profile data"}