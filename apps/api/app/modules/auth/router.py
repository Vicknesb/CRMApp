from fastapi import APIRouter, Cookie, Depends, Request, Response, status
from prisma import Prisma

from app.core.audit import record_audit
from app.core.dependencies import get_current_user
from app.core.envelope import err, ok
from app.core.security import COOKIE_MAX_AGE, COOKIE_NAME
from app.db.client import get_db
from app.modules.auth import service
from app.modules.auth.schemas import (
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RegisterRequest,
    TwoFAVerifyRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: Prisma = Depends(get_db)) -> dict:
    session = await service.register(db, body.email, body.password, body.firstName, body.lastName)
    return ok(session.model_dump())


@router.post("/login")
async def login(body: LoginRequest, response: Response, db: Prisma = Depends(get_db)) -> dict:
    session, token = await service.login(db, body.email, body.password, body.totpCode)
    if session.requires2FA:
        return ok(session.model_dump())
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=COOKIE_MAX_AGE,
        secure=False,  # True in production with TLS
    )
    await record_audit(db, session.id, "LOGIN", "auth", record_id=session.id)
    return ok(session.model_dump())


@router.post("/logout")
async def logout(
    response: Response,
    db: Prisma = Depends(get_db),
    crm_access_token: str | None = Cookie(default=None, alias=COOKIE_NAME),
) -> dict:
    if crm_access_token:
        await service.logout(db, crm_access_token)
    response.delete_cookie(COOKIE_NAME)
    return ok({"message": "Logged out"})


@router.get("/session")
async def session(
    db: Prisma = Depends(get_db),
    crm_access_token: str | None = Cookie(default=None, alias=COOKIE_NAME),
) -> dict:
    if not crm_access_token:
        return err("Not authenticated")
    sess = await service.get_session(db, crm_access_token)
    return ok(sess.model_dump())


@router.post("/2fa/setup")
async def setup_2fa(
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
) -> dict:
    result = await service.setup_2fa(db, current_user.id)
    return ok(result)


@router.post("/2fa/verify")
async def verify_2fa(
    body: TwoFAVerifyRequest,
    current_user=Depends(get_current_user),
    db: Prisma = Depends(get_db),
) -> dict:
    await service.verify_2fa(db, current_user.id, body.code)
    await record_audit(db, current_user.id, "2FA_ENABLED", "auth", record_id=current_user.id)
    return ok({"enabled": True})


@router.post("/password-reset/request")
async def request_reset(body: PasswordResetRequest, db: Prisma = Depends(get_db)) -> dict:
    await service.request_password_reset(db, body.email)
    return ok({"message": "If the email exists a reset link has been sent"})


@router.post("/password-reset/confirm")
async def confirm_reset(body: PasswordResetConfirm, db: Prisma = Depends(get_db)) -> dict:
    await service.confirm_password_reset(db, body.token, body.newPassword)
    return ok({"message": "Password reset successfully"})
