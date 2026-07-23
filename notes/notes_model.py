from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class Note(Base):
    __tablename__ = "notes"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str]
    content : Mapped[str]


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str