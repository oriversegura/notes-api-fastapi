from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user import user_model


async def get_all(db: AsyncSession) -> Sequence[user_model.User]:
    """Return all users."""
    result = await db.execute(select(user_model.User))
    return result.scalars().all()

async def get_by_id(db: AsyncSession, user_id: int) -> user_model.User | None:
    """Return a user by id."""
    result = await db.execute(
        select(user_model.User).where(user_model.User.id == user_id)
    )
    return result.scalars().first()

async def get_by_email(db: AsyncSession, email: str) -> user_model.User | None:
    """Return a user by email."""
    result = await db.execute(
        select(user_model.User).where(user_model.User.email == email)
    )
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: user_model.UserCreate) -> user_model.User:
    """Create a new user."""
    new_user = user_model.User(
        name=user_in.name,
        surname=user_in.surname,
        email=user_in.email,
        hashed_password=user_in.password,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(
    db: AsyncSession,
    user_id: int,
    user_in: user_model.UserCreate,
) -> user_model.User | None:
    """Update an existing user."""
    result = await db.execute(
        select(user_model.User).where(user_model.User.id == user_id)
    )

    user_to_update = result.scalars().first()

    if user_to_update is None:
        return None

    user_to_update.name = user_in.name
    user_to_update.surname = user_in.surname
    user_to_update.email = user_in.email
    user_to_update.hashed_password = user_in.password

    await db.commit()
    await db.refresh(user_to_update)
    return user_to_update

async def delete_user(db: AsyncSession, user_id: int) -> user_model.User | None:
    """Delete a user by id."""
    result = await db.execute(
        select(user_model.User).where(user_model.User.id == user_id)
    )
    user_to_delete = result.scalars().first()
    if user_to_delete is None:
        return None
    await db.delete(user_to_delete)
    await db.commit()
    await db.refresh(user_to_delete)
    return user_to_delete