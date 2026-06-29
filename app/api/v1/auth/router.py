from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import (
    Token,
    UserCreate,
    UserResponse,
    UserLogin,
)
from app.services.auth_service import AuthService
from app.api.v1.auth.dependencies import get_current_user
from app.db.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:

    service = AuthService(db)

    try:
        return await service.register_user(user)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Token:

    service = AuthService(db)

    try:
        return await service.authenticate_user(credentials)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
    
@router.get(
    "/me",
    response_model=UserResponse,
)
async def me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Return the currently authenticated user.
    """

    return UserResponse.model_validate(current_user)
    
