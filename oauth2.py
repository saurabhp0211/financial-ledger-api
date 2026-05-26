from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from datetime import datetime ,timedelta,timezone
import models
from database import get_db


SECRET_KEY = "SUPER_SECRET_KEY_do_not_share"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire.timestamp()})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception=HTTPException(status_code=401,
                                        detail="Could not validate Credentials",
                                        headers={"WWW-Authenticate":"Bearer"},
                                        )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str=payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user=db.query(models.User).filter(models.User.email==email).first()
    if user is None:
        raise credentials_exception
    return user
