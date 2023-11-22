from sqlalchemy import Boolean, Column, Integer, LargeBinary, String, PrimaryKeyConstraint, UniqueConstraint

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=False, unique=True, index=True)
    hashed_password = Column(LargeBinary, nullable=False)
    username = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)

    UniqueConstraint(email, name="uix_email")
    PrimaryKeyConstraint(id, name="pk_user_id")

    def __repr__(self):
        return f"<User {self.username}>"
