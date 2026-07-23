from http.client import HTTPException
from unittest import result

from notes.notes_model import Note, NoteCreate, NoteResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Get all notes
async def get_all(db: AsyncSession):
    result = await db.execute(select(Note))
    return result.scalars().all()

# Get notes by id
async def get_by_id(db: AsyncSession, note_id: int):
    result = await db.execute(select(Note).where(Note.id == note_id))
    return result.scalars().first()

# Create notes
async def create_note(db: AsyncSession, note: NoteCreate):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note

# Update Notes
async def update_note(db: AsyncSession, note_id: int, note: NoteCreate):
    result = await db.execute(select(Note).where(Note.id == note_id))

    note_to_update = (result.scalars().first())

    if note_to_update is None:
        return None

    note_to_update.title = note.title
    note_to_update.content = note.content

    await db.commit()
    await db.refresh(note_to_update)
    return note_to_update

# Delete Notes
async def delete_note(db: AsyncSession, note_id: int):
    result = await db.execute(select(Note).where(Note.id == note_id))
    note_to_delete = (result.scalars().first())
    if note_to_delete is None:
        return None
    await db.delete(note_to_delete)
    await db.commit()
    return note_to_delete



