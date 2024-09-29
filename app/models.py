"""models using sqlalchemy"""
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime, column


class Base(DeclarativeBase):
    """Base class from declarativeBase to be used as model class's parent"""
    pass


class User(Base):
    """user model class"""
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200))
    fullname: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r})"


class Post(Base):
    """post model class"""
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(2000))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"post(id={self.id!r}, body={self.body!r})"


class Session(Base):
    """session class model"""
    __tablename__ = "session"
    session_key: Mapped[str] = mapped_column(primary_key=True)
    session_value: Mapped[str] = mapped_column(String(1000))
    expire_date = column(DateTime)


# my(Amir) models just for reference:

# from datetime import datetime, timedelta
# import uuid

# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
# from sqlalchemy.orm import relationship, declarative_base

# Base = declarative_base()

# class User(Base):
#     """User Model Class"""
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     password = Column(String)
#     last_login = Column(DateTime)

# class Post(Base):
#     """Post Model Class"""
#     __tablename__ = "posts"
#     id = Column(Integer, primary_key=True)
#     author = Column(Integer, ForeignKey('users.id'), nullable=False)
#     title = Column(String)
#     body = Column(String)
#     created_at = Column(DateTime)

# class Session(Base):
#     """Session Model Class"""
#     __tablename__ = "sessions"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     token = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
#     created_at = Column(DateTime, default=datetime.utcnow)
#     expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=1))

# engine = create_engine('sqlite:///proj/example.db')
# Base.metadata.create_all(engine)
# print('db created!')
