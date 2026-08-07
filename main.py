"""Main entrypoint for the Notes API application."""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from auth.auth_router import router as auth_router
from database.database import Base, engine
from notes.notes_router import router as notes_router
from user.user_router import router as user_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    """Manage the application lifespan, creating database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app : FastAPI = FastAPI(title="Notes API", version="0.0.1", lifespan=lifespan)

@app.get("/")
def read_root() -> dict[str, str]:
    """Return a simple status message for the API root."""
    return {"This api": "Stil Alive"}

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(notes_router)

def main() -> None:
    """Start the FastAPI server using Uvicorn."""
    port = int(os.environ.get('PORT', 8000))
    print(f'Server running on http://127.0.0.1:{port}')
    uvicorn.run(app, host='127.0.0.1', port=port)

if __name__ == "__main__":
    main()
