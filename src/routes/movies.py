import math
from typing import Optional

from fastapi import (APIRouter, Depends,
                     HTTPException, Query, Request)
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def list_movies(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db),
):
    # total count
    total_result = await db.execute(select(func.count()).select_from(MovieModel))
    total_items = int(total_result.scalar() or 0)

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = math.ceil(total_items / per_page)

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page
    q = select(MovieModel).order_by(MovieModel.id).offset(offset).limit(per_page)
    result = await db.execute(q)
    movies = result.scalars().all()

    for i in range(0, len(movies)):
        movies[i].date = movies[i].date.strftime("%Y-%m-%d") if movies[i].date else None

    required_path = "/theater/movies/"
    prev_page: Optional[str] = (
        f"{required_path}?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page: Optional[str] = (
        f"{required_path}?page={page + 1}&per_page={per_page}" if page < total_pages else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    q = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(q)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    if movie.date:
        movie.date = movie.date.strftime("%Y-%m-%d")

    return movie
