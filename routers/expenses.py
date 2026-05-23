from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional, List
import jwt

import models
from database import get_db
from schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate


router=APIRouter(
    prefix="/expenses",
    tags=["Ledger Transactions"]
)


SECRET_KEY="SUPER_SECRET_KEY_do_not_share"
ALGORITHM = "HS256"

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


