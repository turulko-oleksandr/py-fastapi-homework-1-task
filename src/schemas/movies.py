# Write your code here
from typing import Optional, List
from pydantic import BaseModel


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str | None = None
    date: str | None = None
    score: float | None = None
    genre: str | None = None
    overview: str | None = None
    crew: str | None = None
    orig_title: str | None = None
    status: str | None = None
    orig_lang: str | None = None
    budget: float | None = None
    revenue: float | None = None
    country: str | None = None

    class Config:
        orm_mode = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int

    class Config:
        orm_mode = True
