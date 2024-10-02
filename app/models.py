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
    post: Mapped[list["Post"]] =relationship (
        back_populates='user' , cascade='all , delete-orphan'
    )
    last_login : Mapped[Optional[str]]
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r} , last_lagin={self.last_login!r} , email={self.email!r})"

class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    author : Mapped[str] = mapped_column(String(20),ForeignKey('user_account.id'))
    title : Mapped[str] = mapped_column(String(20))
    body:Mapped[str] = mapped_column(String(2000))
    created_at:Mapped[DateTime]=mapped_column(DateTime(1000))
    user: Mapped["User"] = relationship(back_populates="post")
    def __repr__(self) -> str:
        return f"post(id={self.id!r}, body={self.body!r})"
    
class Session(Base):
    __tablename__="session"
    session_key:Mapped[str]=mapped_column(primary_key=True)
    session_value:Mapped[str]=mapped_column(String(1000))
    expire_date : Mapped[DateTime]=mapped_column(DateTime(1000))
