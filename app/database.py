from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings as s

SQLALCHEMY_DATABASE_URL = f"postgresql://{s.database_username}:{s.database_password}@{s.database_hostname}/{s.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password=1234, cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database connected Successfully!")
# except Exception as e:
#     print("Database Connection Failed!")
#     print("Error:", e)