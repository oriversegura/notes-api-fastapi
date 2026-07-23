from user.user_model import User, UserCreate, UserResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Get all Users
async def get_all(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

# Get Users by id
async def get_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

# Get User by Email
async def get_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )

    return result.scalars().first()

# Create Users
async def create_user(db: AsyncSession, user: UserCreate):
    new_user = User(name=user.name, surname=user.surname, email=user.email, hashed_password=user.password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# Update Users
async def update_user(db: AsyncSession, user_id: int, user: UserCreate):
    result = await db.execute(select(User).where(User.id == user_id))

    user_to_update = (result.scalars().first())

    if user_to_update is None:
        return None

    user_to_update.name = user.name
    user_to_update.surname = user.surname
    user_to_update.email = user.email
    user_to_update.hashed_password = user.password

    await db.commit()
    await db.refresh(user_to_update)
    return user_to_update

# Delete Users
async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user_to_delete = result.scalars().first()
    if user_to_delete is None:
        return None
    await db.delete(user_to_delete)
    await db.commit()
    await db.refresh(user_to_delete)
    return user_to_delete