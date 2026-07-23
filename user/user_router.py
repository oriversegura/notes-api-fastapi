from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from user import user_repository
from user.user_model import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_repository.get_all(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int,
                   db: AsyncSession = Depends(get_db)
                   ):
    user = await user_repository.get_by_id(db, user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/", response_model=UserResponse)
async def create_user( user: UserCreate,
                       db: AsyncSession = Depends(get_db)
                       ):
    return await user_repository.create_user(db, user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int,
                      user: UserCreate,
                      db: AsyncSession = Depends(get_db)
                      ):
    updated_user = await user_repository.update_user(db, user_id, user)

    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted_user = await user_repository.delete_user(db, user_id)

    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted"}