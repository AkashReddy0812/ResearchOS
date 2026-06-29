from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class UserCreate(BaseModel):
    full_name: str = Field(
        min_length=3,
        max_length=100,
        description="User's full name",
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password",
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:

        if not any(c.isupper() for c in value):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not any(c.islower() for c in value):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )

        if not any(c.isdigit() for c in value):
            raise ValueError(
                "Password must contain at least one digit."
            )

        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )