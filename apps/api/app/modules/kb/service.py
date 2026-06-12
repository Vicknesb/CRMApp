from datetime import datetime, timezone
from prisma import Prisma
from app.core.audit import record_audit
from app.middleware.error_handler import NotFoundError
from app.modules.kb.schemas import ArticleCreate, ArticleRatingCreate, ArticleUpdate


async def create_article(db: Prisma, body: ArticleCreate, author_id: str) -> object:
    data = body.model_dump(exclude_none=True)
    data["authorId"] = author_id
    article = await db.kbarticle.create(data=data)
    await record_audit(db, author_id, "CREATE", "kbArticles", record_id=article.id, new_values=data)
    return article


async def get_article(db: Prisma, article_id: str) -> object:
    article = await db.kbarticle.find_first(where={"id": article_id, "deletedAt": None})
    if not article:
        raise NotFoundError(f"Article {article_id} not found")
    # Increment view count
    await db.kbarticle.update(where={"id": article_id}, data={"views": {"increment": 1}})
    return article


async def list_articles(db: Prisma, category_id: str | None, search: str | None,
                        published_only: bool, page: int, page_size: int) -> tuple[list, int]:
    where: dict = {"deletedAt": None}
    if published_only:
        where["isPublished"] = True
    if category_id:
        where["categoryId"] = category_id
    if search:
        where["OR"] = [
            {"title": {"contains": search, "mode": "insensitive"}},
            {"body": {"contains": search, "mode": "insensitive"}},
        ]
    skip = (page - 1) * page_size
    articles = await db.kbarticle.find_many(where=where, skip=skip, take=page_size,
                                            order={"createdAt": "desc"})
    total = await db.kbarticle.count(where=where)
    return articles, total


async def update_article(db: Prisma, article_id: str, body: ArticleUpdate, actor_id: str) -> object:
    await get_article(db, article_id)
    data = body.model_dump(exclude_none=True)
    updated = await db.kbarticle.update(where={"id": article_id}, data=data)
    await record_audit(db, actor_id, "UPDATE", "kbArticles", record_id=article_id, new_values=data)
    return updated


async def delete_article(db: Prisma, article_id: str, actor_id: str) -> None:
    await get_article(db, article_id)
    await db.kbarticle.update(where={"id": article_id},
                              data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "kbArticles", record_id=article_id)


async def rate_article(db: Prisma, article_id: str, body: ArticleRatingCreate, user_id: str) -> object:
    await get_article(db, article_id)
    rating = await db.articlerating.upsert(
        where={"articleId_userId": {"articleId": article_id, "userId": user_id}},
        data={
            "create": {"articleId": article_id, "userId": user_id, "helpful": body.helpful},
            "update": {"helpful": body.helpful},
        },
    )
    return rating


async def suggest_for_ticket(db: Prisma, ticket_subject: str, limit: int = 5) -> list:
    """Simple keyword-based suggestion: search article titles/body against ticket subject words."""
    words = [w for w in ticket_subject.split() if len(w) > 3]
    if not words:
        return await db.kbarticle.find_many(where={"isPublished": True, "deletedAt": None},
                                            take=limit, order={"views": "desc"})
    or_clauses = [{"title": {"contains": w, "mode": "insensitive"}} for w in words]
    return await db.kbarticle.find_many(
        where={"isPublished": True, "deletedAt": None, "OR": or_clauses},
        take=limit,
        order={"views": "desc"},
    )
