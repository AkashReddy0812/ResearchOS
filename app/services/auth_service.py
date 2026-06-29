from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.db.models.user import User
from app.schemas.auth import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)


class AuthService:
    """
    Handles all authentication-related business logic.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email.
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()
    

    async def register_user(
    self,
    user_data: UserCreate,
    ) -> UserResponse:
        """
        Register a new user.
        """

        existing_user = await self.get_user_by_email(user_data.email)

        if existing_user:
            raise ValueError("A user with this email already exists.")

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return UserResponse.model_validate(user)    

    async def authenticate_user(
    self,
    credentials: UserLogin,
    ) -> Token:
        """
        Authenticate a user and return a JWT access token.
        """

        user = await self.get_user_by_email(credentials.email)

        if not user:
            raise ValueError("Invalid email or password.")

        if not verify_password(
            credentials.password,
            user.hashed_password,
        ):
            raise ValueError("Invalid email or password.")

        access_token = create_access_token(
            subject=user.email,
        )

        return Token(
            access_token=access_token,
        )