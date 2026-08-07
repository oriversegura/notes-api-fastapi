"""Notes models for the application."""

from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Note(Base):
    """ORM model for notes."""
    __tablename__ = "notes"

    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str]
    content : Mapped[str]

    def __repr__(self) -> str:
        return f"<Note id={self.id!r} title={self.title!r}>"


class NoteCreate(BaseModel):
    """Schema for creating a note."""
    title: str
    content: str


class NoteResponse(BaseModel):
    """Schema for note response."""
    id: int
    title: str
    content: str
