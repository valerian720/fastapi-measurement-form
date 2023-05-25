from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

user=os.environ.get("DATABASE_USERNAME")
password=os.environ.get("DATABASE_PASSWORD")
database = os.environ.get("DATABASE")
host=os.getenv("DATABASE_HOST")
port=os.getenv("DATABASE_PORT")
# sqlite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# docker db
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4" # or "mysql+pymysql://db_username:user_password@localhost/test"
# local db
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root@localhost/test" # or "mysql+pymysql://db_username:user_password@localhost/test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # , connect_args={"check_same_thread": False} # only for sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()