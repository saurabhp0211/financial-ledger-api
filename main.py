from fastapi import FastAPI,Depends,HTTPException
from schemas import ExpenseCreate, ExpenseResponse,ExpenseUpdate,UserResponse,UserCreate
from sqlalchemy.orm import Session
from typing import Optional
from typing import List
from utils import hash_password
import models
from database import engine, get_db



models.Base.metadata.create_all(bind=engine)


app=FastAPI(title="Saurabh's Expense Tracker")


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Expense Tracker API",
        "version":"1.0.0"
    }

@app.post("/users",response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    db_user=db.query(models.User).filter(models.User.email==user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    

    hashed_pwd=hash_password(user.password)
    new_user=models.User(email=user.email, hashed_password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}",response_model=UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user





@app.get("/expenses",response_model=list[ExpenseResponse])
def get_expenses(category:Optional[str]=None, db: Session=Depends(get_db)):
    query=db.query(models.Expense)

    if category:
        query=query.filter(models.Expense.category==category)
    
    return query.all()
                           
    
                   

  
@app.post("/expenses", response_model=ExpenseResponse)
def create_expense(expense:ExpenseCreate,db:Session=Depends(get_db)):

    user=db.query(models.User).filter(models.User.id==expense.owner_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {expense.owner_id} does not exist")

    new_expense=models.Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        expense_date=expense.expense_date,
        owner_id=expense.owner_id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@app.patch("/expenses/{expense_id}",response_model=ExpenseResponse)
def update_expense(expense_id:int,updated_data:ExpenseUpdate,db:Session=Depends(get_db)):
    db_expense=db.query(models.Expense).filter(models.Expense.id==expense_id).first()

    if not db_expense:
        raise HTTPException(status_code=404,detail="Expense not found")
    
    update_dict=updated_data.model_dump(exclude_unset=True)

    for key,value in update_dict.items():
        setattr(db_expense,key,value)
    
    db.commit()
    db.refresh(db_expense)

    return db_expense

@app.get("/users",response_model=List[UserResponse])
def read_users(skip:int=0,limit:int=100, db: Session=Depends(get_db)):
    users=db.query(models.User).offset(skip).limit(limit).all()
    return users

    


                                  