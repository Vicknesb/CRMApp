from fastapi import Cookie, Depends
from prisma import Prisma
from prisma.models import User

from app.core.enums import UserRole
from app.core.security import decode_token, COOKIE_NAME
from app.db.client import get_db
from app.middleware.error_handler import ForbiddenError, UnauthorizedError
from app.modules.auth import repository as repo


async def get_current_user(
    db: Prisma = Depends(get_db),
    crm_access_token: str | None = Cookie(default=None, alias=COOKIE_NAME),
) -> User:
    if not crm_access_token:
        raise UnauthorizedError("Not authenticated")
    try:
        payload = decode_token(crm_access_token)
    except ValueError:
        raise UnauthorizedError("Invalid or expired token")
    user_id: str = payload.get("sub", "")
    user = await repo.find_user_by_id(db, user_id)
    if not user or not user.isActive:
        raise UnauthorizedError("User not found or inactive")
    return user


def require_role(*roles: UserRole):
    async def guard(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise ForbiddenError(
                f"Role {current_user.role} does not have access to this resource"
            )
        return current_user
    return guard
