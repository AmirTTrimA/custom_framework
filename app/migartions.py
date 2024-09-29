"""migrations from sqlalchemy to sqlite3"""
from sqlalchemy import create_engine
from app.models import Base

engine = create_engine("sqlite:///db.sqlite3", echo=True)
if __name__ == "__main__":
    Base.metadata.create_all(engine)
