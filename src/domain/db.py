from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import DB_URL

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

__all__ = ["engine", "Session", "Base"]

class Base(DeclarativeBase):
    ...