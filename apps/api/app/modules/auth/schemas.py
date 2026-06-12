from pydantic import BaseModel, EmailStr, field_validator
from app.core.enums import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    totpCode: str | None = None


class SessionResponse(BaseModel):
    id: str
    email: str
    firstName: str
    lastName: str
    role: UserRole
    requires2FA: bool = False


class TwoFASetupResponse(BaseModel):
    secret: str
    otpauthUrl: str
    qrCodeUrl: str


class TwoFAVerifyRequest(BaseModel):
    code: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    newPassword: str

    @field_validator("newPassword")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v
