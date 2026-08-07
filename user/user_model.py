from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class User(Base):
    """SQLAlchemy model for application users."""

    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    surname : Mapped[str]
    email : Mapped[str]
    hashed_password : Mapped[str]

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    name: str
    surname: str
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    """Schema for returning user data in responses."""

    id: int
    name: str
    surname: str
    email: EmailStr

    