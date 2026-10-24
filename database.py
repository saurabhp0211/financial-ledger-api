from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL= "sqlite:///./expenses.db"

engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

@event.listens_for(Engine,"connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor=dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally: 
        db.close()


venv) saurabhkumarpandey@Saurabhs-MacBook-Air equipay-backend % git grep -n "DATABASE_URL" HEAD
HEAD:alembic.ini:89:# SQLALCHEMY_DATABASE_URL = "sqlite:///./expenses.db"
HEAD:database.py:7:# SQLALCHEMY_DATABASE_URL = "sqlite:///./expenses.db"
HEAD:database.py:8:SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@db:5432/equipay_db"
HEAD:database.py:10:engine=create_engine(SQLALCHEMY_DATABASE_URL)
HEAD:docker-compose.yml:26:      - DATABASE_URL=postgresql://postgres:password123@db:5432/equipay_db
(venv) saurabhkumarpandey@Saurabhs-MacBook-Air equipay-backend % 
