from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from notes import notes_repository
from notes.notes_model import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes")


@router.get("/", response_model=list[NoteResponse])
async def get_notes(db: AsyncSession = Depends(get_db)) -> list[NoteResponse]:
    return await notes_repository.get_all(db)

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int,
                   db: AsyncSession = Depends(get_db)
                   ):
    note = await notes_repository.get_by_id(db, note_id)

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.post("/", response_model=NoteResponse)
async def create_note( note: NoteCreate,
                       db: AsyncSession = Depends(get_db)
                       ) -> NoteResponse:
    return await notes_repository.create_note(db, note)

@router.put("/{id}", response_model=NoteResponse)
async def update_note(note_id: int,
                      note: NoteCreate,
                      db: AsyncSession = Depends(get_db)
                      ) -> NoteResponse:
    updated_note = await notes_repository.update_note(db, note_id, note)

    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return updated_note
