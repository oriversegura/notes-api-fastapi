"""Notes router endpoints for the Notes API."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from notes import notes_repository
from notes.notes_model import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes")
db_dependency = Depends(get_db)


@router.get("/", response_model=list[NoteResponse])
async def get_notes(db: AsyncSession = db_dependency) -> list[NoteResponse]:
    """Retrieve all notes from the database."""
    notes = await notes_repository.get_all(db)
    return [NoteResponse.model_validate(note) for note in notes]

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int,
                   db: AsyncSession = db_dependency
                   ) -> NoteResponse:
    """Retrieve a specific note by its ID."""
    note = await notes_repository.get_by_id(db, note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return NoteResponse.model_validate(note)


@router.post("/", response_model=NoteResponse)
async def create_note(note: NoteCreate,
                       db: AsyncSession = db_dependency
                       ) -> NoteResponse:
    """Create a new note."""
    created_note = await notes_repository.create_note(db, note)
    return NoteResponse.model_validate(created_note)

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int,
                      note: NoteCreate,
                      db: AsyncSession = db_dependency
                      ) -> NoteResponse:
    """Update an existing note by its ID."""
    updated_note = await notes_repository.update_note(db, note_id, note)

    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return NoteResponse.model_validate(updated_note)
