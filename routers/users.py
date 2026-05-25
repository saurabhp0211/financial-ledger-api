from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta, timezone
import jwt

import models
from database import get_db
from schemas import UserCreate, UserResponse
from utils import hash_password, verify_pw

router= APIRouter(tags=["Identity & Authentication"])

SECRET_KEY = "SUPER_SECRET_KEY_do_not_share"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/users",response_model=UserResponse)
def create_user(user: UserCreate,db:Session=Depends(get_db)):
    db_user=db.query(models.User).filter(models.User.email==user.email).first()

    if db_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    
    hashed_pwd=hash_password(user.password)
    new_user=models.User(email=user.email,hashed_password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{user_id}",response_model=UserResponse)
def get_user(user_id:int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user


@router.get("/users",response_model=List[UserResponse])
def read_users(skip:int=0,limit:int=100, db:Session=Depends(get_db)):
    users=db.query(models.User).offset(skip).limit(limit).all()
    return users


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Email or Password")
    
    if not verify_pw(form_data.password,user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Email or Password")
    
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data={"sub":user.email,"exp":expire}
    encoded_jwt=jwt.encode(token_data,SECRET_KEY,algorithm=ALGORITHM)

    return {"access_token":encoded_jwt,"token_type":"bearer"}
    



