from collections.abc import Sequence

import sqlalchemy
import sqlalchemy.ext.asyncio

from notes.notes_model import Note, NoteCreate


# Get all notes
async def get_all(db: sqlalchemy.ext.asyncio.AsyncSession) -> Sequence[Note]:
    """Return all notes from the database."""
    result = await db.execute(sqlalchemy.select(Note))
    return result.scalars().all()

# Get notes by id
async def get_by_id(db: sqlalchemy.ext.asyncio.AsyncSession, note_id: int) -> Note | None:
    """Get a note by its ID from the database."""
    result = await db.execute(sqlalchemy.select(Note).where(Note.id == note_id))
    return result.scalars().first()

# Create notes
async def create_note(db: sqlalchemy.ext.asyncio.AsyncSession, note: NoteCreate) -> Note:
    """Create and return a new note in the database."""
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note

# Update Notes
async def update_note(db: sqlalchemy.ext.asyncio.AsyncSession, note_id: int, note: NoteCreate) -> Note | None:
    """Update an existing note by its ID and return the updated note."""
    result = await db.execute(sqlalchemy.select(Note).where(Note.id == note_id))

    note_to_update = (result.scalars().first())

    if note_to_update is None:
        return None

    note_to_update.title = note.title
    note_to_update.content = note.content

    await db.commit()
    await db.refresh(note_to_update)
    return note_to_update

# Delete Notes
async def delete_note(db: sqlalchemy.ext.asyncio.AsyncSession, note_id: int) -> Note | None:
    """Delete a note by its ID and return the deleted note."""
    result = await db.execute(sqlalchemy.select(Note).where(Note.id == note_id))
    note_to_delete = (result.scalars().first())
    if note_to_delete is None:
        return None
    await db.delete(note_to_delete)
    await db.commit()
    return note_to_delete



