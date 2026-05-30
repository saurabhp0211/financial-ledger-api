from fastapi import FastAPI
import models
from database import engine
from routers import users,expenses


# models.Base.metadata.create_all(bind=engine)


app=FastAPI(title=("Saurabh's Secure Expense Tracker"))

@app.get("/")
def read_root():
    return{
        "status":"online",
        "message":"Welcome to the clean modular Expense Tracker API",
        "version":"2.0.0"
    }

app.include_router(users.router)
app.include_router(expenses.router)