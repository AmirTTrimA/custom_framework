from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, create_engine
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
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r})"

class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    body:Mapped[str] = mapped_column(String(2000))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    # user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"post(id={self.id!r}, body={self.body!r})"

class Session(Base):
    __tablename__="session"
    session_key:Mapped[str]=mapped_column(primary_key=True)
    session_value:Mapped[str]=mapped_column(String(1000))
    expire_date = column(DateTime)

# class Address(Base):
#     __tablename__ = 'addresses'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(String(200))
#     user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
#     user: Mapped["User"] = relationship(back_populates="addresses")

engine = create_engine("sqlite:///db.sqlite3", echo=True)
Base.metadata.create_all(engine)


from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)

# def add_post(user_id: int, body: str):
#     # Create a new session
#     session = SessionLocal()
#     try:
#         # Create a new Post instance
#         new_post = Post(body=body, user_id=user_id)
        
#         # Add the post to the session
#         session.add(new_post)
        
#         # Commit the session to save the post
#         session.commit()
        
#         print(f"Post added: {new_post}")
#     except Exception as e:
#         # Rollback the session in case of error
#         session.rollback()
#         print(f"Error occurred: {e}")
#     finally:
#         # Close the session
#         session.close()

# # Example usage
# add_post(user_id=1, body="This is a new post!")
