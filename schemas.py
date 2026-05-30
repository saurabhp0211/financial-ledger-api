from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date,datetime


# the base schema where we define what exactly goes inside the expense record we are updating
class ExpenseBase(BaseModel):
    title: str=Field(..., min_length=3, max_length=50, example="Starbucks Coffee")
    amount: float= Field(..., gt=0, example=250.75)
    category: str= Field(..., example="Food")
    expense_date: Optional[date]= Field(default_factory=date.today)

class UserBase(BaseModel):
    email:EmailStr



# input from the user
class UserCreate(UserBase):
    password:str
    phone_number:Optional[str]=None

class ExpenseCreate(ExpenseBase):
    pass


# Schema for reading an expense
class UserResponse(UserBase):
    id:int
    phone_number:Optional[str]=None
    created_at:datetime


    class Config:
        from_attributes=True


class ExpenseResponse(ExpenseBase):
    id:int
    owner_id:int
    created_at: datetime
    owner: UserResponse

    class Config:
        from_attributes=True

class ExpenseUpdate(BaseModel):
    title: Optional[str]=None
    amount: Optional[float]=None
    category:Optional[str]=None
    expense_date: Optional[date]=None








