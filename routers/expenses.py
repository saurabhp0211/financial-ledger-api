from fastapi import APIRouter, Depends, HTTPException
import oauth2
from sqlalchemy.orm import Session
from typing import Optional, List


import models
from database import get_db
from schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate


router=APIRouter(
    prefix="/expenses",
    tags=["Ledger Transactions"]
)


@router.post("", response_model=ExpenseResponse)
def create_expense(
    expense:ExpenseCreate,
    db: Session=Depends(get_db),
    current_user: models.User=Depends(oauth2.get_current_user)
):
    new_expense=models.Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        expense_date=expense.expense_date,
        owner_id=current_user.id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("",response_model=List[ExpenseResponse])
def get_expenses(
    category:Optional[str]=None,
    skip:int=0,
    limit:int=100,
    db:Session=Depends(get_db),
    current_user: models.User=Depends(oauth2.get_current_user)

):

    query=db.query(models.Expense).filter(models.Expense.owner_id==current_user.id)

    if category:
        query=query.filter(models.Expense.category==category)

    return query.offset(skip).limit(limit).all()

@router.patch("/{expense_id}",response_model=ExpenseResponse)
def update_expense(
    expense_id:int,
    updated_data:ExpenseUpdate,
    db:Session=Depends(get_db),
    current_user:models.User=Depends(oauth2.get_current_user)
):
    
    db_expense=db.query(models.Expense).filter(
        models.Expense.id==expense_id,
        models.Expense.owner_id==current_user.id
    ).first()

    if not db_expense:
        raise HTTPException(status_code=404,detail="Expense record not found")
    
    update_dict=updated_data.model_dump(exclude_unset=True)

    for key,value in update_dict.items():
        setattr(db_expense,key,value)

    db.commit()
    db.refresh(db_expense)
    return db_expense




