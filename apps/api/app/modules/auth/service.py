import base64
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import pyotp
from prisma import Prisma

from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.middleware.error_handler import NotFoundError, UnauthorizedError
from app.modules.auth import repository as repo
from app.modules.auth.schemas import SessionResponse


async def register(db: Prisma, email: str, password: str,
                   first_name: str, last_name: str) -> SessionResponse:
    existing = await repo.find_user_by_email(db, email)
    if existing:
        raise ValueError("Email already registered")
    hashed = hash_password(password)
    user = await repo.create_user(db, email, hashed, first_name, last_name)
    return SessionResponse(
        id=user.id, email=user.email,
        firstName=user.firstName, lastName=user.lastName, role=user.role,
    )


async def login(db: Prisma, email: str, password: str,
                totp_code: str | None) -> tuple[SessionResponse, str]:
    user = await repo.find_user_by_email(db, email)
    if not user or not verify_password(password, user.passwordHash):
        raise UnauthorizedError("Invalid email or password")

    totp_rec = await repo.find_totp_secret(db, user.id)
    if totp_rec and totp_rec.enabled:
        if not totp_code:
            return SessionResponse(
                id=user.id, email=user.email,
                firstName=user.firstName, lastName=user.lastName,
                role=user.role, requires2FA=True,
            ), ""
        totp = pyotp.TOTP(totp_rec.secret)
        if not totp.verify(totp_code, valid_window=1):
            raise UnauthorizedError("Invalid 2FA code")

    token = create_access_token({"sub": user.id, "role": user.role})
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    await repo.create_session(db, user.id, token, expires_at)

    return SessionResponse(
        id=user.id, email=user.email,
        firstName=user.firstName, lastName=user.lastName, role=user.role,
    ), token


async def logout(db: Prisma, token: str) -> None:
    await repo.delete_session(db, token)


async def get_session(db: Prisma, token: str) -> SessionResponse:
    payload = decode_token(token)
    user_id: str = payload.get("sub", "")
    user = await repo.find_user_by_id(db, user_id)
    if not user:
        raise UnauthorizedError("Session invalid")
    return SessionResponse(
        id=user.id, email=user.email,
        firstName=user.firstName, lastName=user.lastName, role=user.role,
    )


async def setup_2fa(db: Prisma, user_id: str) -> dict:
    user = await repo.find_user_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")
    secret = pyotp.random_base32()
    await repo.upsert_totp_secret(db, user_id, secret, enabled=False)
    totp = pyotp.TOTP(secret)
    otp_url = totp.provisioning_uri(user.email, issuer_name="CRM Ideas2IT")
    return {
        "secret": secret,
        "otpauthUrl": otp_url,
        "qrCodeUrl": f"https://api.qrserver.com/v1/create-qr-code/?data={otp_url}&size=200x200",
    }


async def verify_2fa(db: Prisma, user_id: str, code: str) -> bool:
    rec = await repo.find_totp_secret(db, user_id)
    if not rec:
        raise NotFoundError("2FA not set up")
    totp = pyotp.TOTP(rec.secret)
    if not totp.verify(code, valid_window=1):
        raise UnauthorizedError("Invalid TOTP code")
    await repo.upsert_totp_secret(db, user_id, rec.secret, enabled=True)
    return True


async def request_password_reset(db: Prisma, email: str) -> str:
    user = await repo.find_user_by_email(db, email)
    if not user:
        return ""  # Silent — don't reveal existence
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expires = datetime.now(timezone.utc) + timedelta(hours=1)
    await repo.store_reset_token(db, user.id, token_hash, expires)
    return token


async def confirm_password_reset(db: Prisma, token: str, new_password: str) -> None:
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    log = await db.auditlog.find_first(
        where={
            "action": "PASSWORD_RESET_REQUEST",
            "module": "auth",
        },
        order={"createdAt": "desc"},
    )
    if not log or not log.newValues:
        raise UnauthorizedError("Invalid or expired reset token")
    stored = log.newValues
    if stored.get("tokenHash") != token_hash:
        raise UnauthorizedError("Invalid or expired reset token")
    from datetime import datetime
    expiry = datetime.fromisoformat(stored["expiresAt"])
    if datetime.now(timezone.utc) > expiry:
        raise UnauthorizedError("Reset token has expired")
    hashed = hash_password(new_password)
    await db.user.update(
        where={"id": log.userId},
        data={"passwordHash": hashed},
    )
