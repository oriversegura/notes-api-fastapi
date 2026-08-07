from collections.abc import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from user import user_repository
from user.user_model import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

db_dependency = Depends(get_db)


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = db_dependency) -> Sequence[UserResponse]:
    """Retrieve all users."""
    users = await user_repository.get_all(db)
    return [UserResponse.model_validate(u) for u in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = db_dependency) -> UserResponse:
    """Retrieve a user by ID."""
    user = await user_repository.get_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.model_validate(user)


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = db_dependency) -> UserResponse:
    """Create a new user."""
    created = await user_repository.create_user(db, user)
    return UserResponse.model_validate(created)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = db_dependency) -> UserResponse:
    """Update an existing user."""
    updated_user = await user_repository.update_user(db, user_id, user)

    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.model_validate(updated_user)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = db_dependency) -> dict[str, str]:
    """Delete a user by ID."""
    deleted_user = await user_repository.delete_user(db, user_id)

    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted"}