from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime,column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200))
    fullname: Mapped[Optional[str]]
    post: Mapped['Post'] = relationship(back_populates="user",cascade="all, delete-orphan")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r})"

class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    body:Mapped[str] = mapped_column(String(2000))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user_name: Mapped[int] = mapped_column(String(30))
    user: Mapped["User"] = relationship( back_populates="post")
    def __repr__(self) -> str:
        return f"post(id={self.id!r}, body={self.body!r})"
    
class Session(Base):
    __tablename__="session"
    session_key:Mapped[str]=mapped_column(primary_key=True)
    session_value:Mapped[str]=mapped_column(String(1000))
    expire_date:Mapped[DateTime] = mapped_column(DateTime)