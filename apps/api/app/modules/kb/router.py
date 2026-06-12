from fastapi import APIRouter, Depends, Query, status
from prisma import Prisma
from typing import Optional

from app.core.dependencies import get_current_user, require_role
from app.core.enums import UserRole
from app.core.envelope import ok
from app.db.client import get_db
from app.modules.kb import service
from app.modules.kb.schemas import ArticleCreate, ArticleRatingCreate, ArticleUpdate

router = APIRouter(prefix="/kb", tags=["knowledge-base"])


@router.post("/articles", status_code=status.HTTP_201_CREATED)
async def create_article(body: ArticleCreate, db: Prisma = Depends(get_db),
                         current_user=Depends(get_current_user)) -> dict:
    return ok((await service.create_article(db, body, current_user.id)).__dict__)


@router.get("/articles")
async def list_articles(
    category_id: Optional[str] = None,
    search: Optional[str] = None,
    published_only: bool = True,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Prisma = Depends(get_db),
    current_user=Depends(get_current_user),
) -> dict:
    articles, total = await service.list_articles(db, category_id, search, published_only, page, page_size)
    return ok([a.__dict__ for a in articles], meta={"total": total, "page": page, "page_size": page_size})


@router.get("/articles/suggest")
async def suggest(subject: str, db: Prisma = Depends(get_db),
                  current_user=Depends(get_current_user)) -> dict:
    articles = await service.suggest_for_ticket(db, subject)
    return ok([a.__dict__ for a in articles])


@router.get("/articles/{article_id}")
async def get_article(article_id: str, db: Prisma = Depends(get_db),
                      current_user=Depends(get_current_user)) -> dict:
    return ok((await service.get_article(db, article_id)).__dict__)


@router.patch("/articles/{article_id}")
async def update_article(article_id: str, body: ArticleUpdate,
                         db: Prisma = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    return ok((await service.update_article(db, article_id, body, current_user.id)).__dict__)


@router.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: str, db: Prisma = Depends(get_db),
                         current_user=Depends(require_role(UserRole.ADMIN))) -> None:
    await service.delete_article(db, article_id, current_user.id)


@router.post("/articles/{article_id}/rate", status_code=status.HTTP_201_CREATED)
async def rate_article(article_id: str, body: ArticleRatingCreate,
                       db: Prisma = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    return ok((await service.rate_article(db, article_id, body, current_user.id)).__dict__)
