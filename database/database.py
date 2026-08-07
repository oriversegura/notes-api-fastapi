"""Database configuration and session dependency."""

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Ruta de la base de datos
DATABASE_URL = "sqlite+aiosqlite:///notes.db"

# Motor de conexión
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Sesiones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


# Clase base para todos los modelos
class Base(DeclarativeBase):
    pass


# Dependency para FastAPI
async def get_db() -> AsyncGenerator[AsyncSession]:
    """Genera una sesión async de la base de datos para dependencias de FastAPI."""
    async with AsyncSessionLocal() as session:
        yield session


