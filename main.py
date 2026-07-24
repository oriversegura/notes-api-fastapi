from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import uvicorn

from database.database import Base, engine

from auth.auth_router import router as auth_router
from user.user_router import router as user_router
from notes.notes_router import router as notes_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app : FastAPI = FastAPI(title="Notes API", version="0.0.1", lifespan=lifespan)

@app.get("/")
def read_root() -> dict[str, str]:
    return {"This api": "Stil Alive"}

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(notes_router)

def main():
    port = int(os.environ.get('PORT', 8000))
    print('Server running on http://127.0.0.1:{}'.format(port))
    uvicorn.run(app, host='127.0.0.1', port=port)

if __name__ == "__main__":
    main()
