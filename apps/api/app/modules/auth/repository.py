from prisma import Prisma
from prisma.models import User


async def find_user_by_email(db: Prisma, email: str) -> User | None:
    return await db.user.find_first(
        where={"email": email, "deletedAt": None}
    )


async def find_user_by_id(db: Prisma, user_id: str) -> User | None:
    return await db.user.find_first(
        where={"id": user_id, "deletedAt": None}
    )


async def create_user(db: Prisma, email: str, password_hash: str,
                      first_name: str, last_name: str) -> User:
    return await db.user.create(data={
        "email": email,
        "passwordHash": password_hash,
        "firstName": first_name,
        "lastName": last_name,
    })


async def find_totp_secret(db: Prisma, user_id: str):
    return await db.twoFactorsecret.find_unique(where={"userId": user_id})


async def upsert_totp_secret(db: Prisma, user_id: str, secret: str, enabled: bool = False):
    return await db.twoFactorsecret.upsert(
        where={"userId": user_id},
        data={
            "create": {"userId": user_id, "secret": secret, "enabled": enabled},
            "update": {"secret": secret, "enabled": enabled},
        },
    )


async def create_session(db: Prisma, user_id: str, token: str, expires_at) -> None:
    await db.session.create(data={
        "userId": user_id,
        "token": token,
        "expiresAt": expires_at,
    })


async def delete_session(db: Prisma, token: str) -> None:
    await db.session.delete_many(where={"token": token})


async def find_session(db: Prisma, token: str):
    return await db.session.find_unique(where={"token": token})


async def store_reset_token(db: Prisma, user_id: str, token_hash: str, expires_at) -> None:
    await db.auditlog.create(data={
        "userId": user_id,
        "action": "PASSWORD_RESET_REQUEST",
        "module": "auth",
        "newValues": {"tokenHash": token_hash, "expiresAt": expires_at.isoformat()},
    })
