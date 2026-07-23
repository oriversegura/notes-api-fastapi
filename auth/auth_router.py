from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from auth.auth import create_access_token, verify_password
from auth.auth_model import LoginRequest, TokenResponse
from database.database import get_db
from user import user_repository

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):

    user = await user_repository.get_by_email(db, login_request.email)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password", headers={"WWW-Authenticate": "Bearer"})

    if not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password", headers={"WWW-Authenticate": "Bearer"})

    token = create_access_token({"sub": user.email, "id": user.id})

    return TokenResponse(access_token=token, token_type="bearer")

