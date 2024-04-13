from typing import List, Self

from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.sql import expression as sql

from app.database import base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hashed_password = Column(String(255), nullable=False)
    username = Column(String(128), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    PrimaryKeyConstraint("id", name="pk_user_id")

    def __repr__(self):
        return f"<User {self.username}>"
    
    @classmethod
    def create(cls, db, **kwargs) -> Self:
        hashed_password = cls.get_password_hash(kwargs.pop('password'))
        kwargs['hashed_password'] = hashed_password
        user = cls(**kwargs)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @classmethod
    def get(cls, db, username) -> Self:
        query = sql.select(cls).where(cls.username == username)
        result = db.execute(query)
        return result.scalars().first()

    @classmethod
    def get_all(cls, db) -> List[Self]:
        query = sql.select(cls)
        result = db.execute(query)
        users = result.scalars().all()
        return users

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
