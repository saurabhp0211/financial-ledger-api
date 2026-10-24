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


(venv) saurabhkumarpandey@Saurabhs-MacBook-Air equipay-backend % docker compose up -d
[+] up 1/3
 ⠙ Container equipay-backend-db-1    Starting                                                        0.2s
 ⠙ Container equipay-backend-redis-1 Starting                                                        0.2s
 ✔ Container equipay-backend-api-1   Recreated                                                       0.1s
Error response from daemon: ports are not available: exposing port TCP 127.0.0.1:6379 -> 127.0.0.1:0: listen tcp4 127.0.0.1:6379: bind: address already in use

What's next:
    Debug this Compose error with Gordon → docker ai "help me fix this compose error"
(venv) saurabhkumarpandey@Saurabhs-MacBook-Air equipay-backend % docker compose up -d
[+] up 1/2
 ✔ Container equipay-backend-redis-1 Started                                                         0.2s
 ⠙ Container equipay-backend-db-1    Starting                                                        0.1s
Error response from daemon: ports are not available: exposing port TCP 127.0.0.1:5432 -> 127.0.0.1:0: listen tcp4 127.0.0.1:5432: bind: address already in use

What's next:
    Debug this Compose error with Gordon → docker ai "help me fix this compose error"
(venv) saurabhkumarpandey@Saurabhs-MacBook-Air equipay-backend % 
