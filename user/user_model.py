from dataclasses import field

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]
    surname : Mapped[str]
    email : Mapped[str]
    hashed_password : Mapped[str]


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr