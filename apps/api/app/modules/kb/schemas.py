from typing import Optional
from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    body: str
    categoryId: Optional[str] = None
    tags: Optional[list[str]] = None
    isPublished: bool = False


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    categoryId: Optional[str] = None
    tags: Optional[list[str]] = None
    isPublished: Optional[bool] = None


class ArticleRatingCreate(BaseModel):
    helpful: bool
