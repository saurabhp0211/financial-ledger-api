from sqlalchemy import Column, Integer,String, Float, Date, ForeignKey
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Expense(Base):
    __tablename__="expenses"
    id = Column(Integer, primary_key=True,index=True,nullable=False)

    title=Column(String,nullable=False)
    amount=Column(Float, nullable=False)
    category=Column(String, nullable=False)
    expense_date=Column(Date, nullable=False)

    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    owner=relationship("User",back_populates="expenses")

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True,nullable=False)
    email=Column(String,nullable=False,unique=True,index=True)
    phone_number=Column(String, nullable=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('CURRENT_TIMESTAMP'))
    hashed_password=Column(String, nullable=False)

    expenses=relationship("Expense",back_populates="owner")