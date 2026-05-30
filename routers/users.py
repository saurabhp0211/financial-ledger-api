from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List


import models
from database import get_db
from schemas import UserCreate, UserResponse
import oauth2
from utils import hash_password, verify_pw

router= APIRouter(tags=["Identity & Authentication"])



@router.post("/users",response_model=UserResponse)
def create_user(user: UserCreate,db:Session=Depends(get_db)):
    db_user=db.query(models.User).filter(models.User.email==user.email).first()

    # if db_user:
    #     raise HTTPException(status_code=400,detail="Email already registered")
    
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
def read_users(skip:int=0,
               limit:int=100,
                db:Session=Depends(get_db),
                current_user: models.User=Depends(oauth2.get_current_user)):
    users=db.query(models.User).offset(skip).limit(limit).all()
    return users


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Email or Password")
    
    if not verify_pw(form_data.password,user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Email or Password")
    
    access_token= oauth2.create_access_token(data={"sub":user.email})
    return {"access_token":access_token, "token_type":"bearer"}



