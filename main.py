from fastapi import FastAPI
import models
from database import engine
from routers import users,expenses

from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


# models.Base.metadata.create_all(bind=engine)    --> Removed the sqlalchemy's create_all to migrate it to alembic


app=FastAPI(title=("Saurabh's Secure Expense Tracker"))

@app.exception_handler(IntegrityError)
async def sqlalchemy_integrity_error_handler(request:Request, exc:IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Database Conflict",
            "message": "This record already exists. For example, this email might already be registered by a user"
        }
    )



@app.get("/")
def read_root():
    return{
        "status":"online",
        "message":"Welcome to the clean modular Expense Tracker API",
        "version":"2.0.0"
    }

app.include_router(users.router)
app.include_router(expenses.router)