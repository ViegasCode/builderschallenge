import httpx
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, cast, Float
from sqlalchemy.ext.asyncio import AsyncSession
from buildbox_challenge_final.models import Movie
from buildbox_challenge_final.schemas import MovieResponse, MovieCreate
from buildbox_challenge_final.database import get_async_db
from buildbox_challenge_final.config import OMDB_API_KEY

router = APIRouter(prefix="/movies", tags=["movies"])

# Busca anos disponíveis
@router.get("/years", response_model=list[str])
async def get_years(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Movie.year).distinct().order_by(Movie.year))
    years = result.scalars().all()
    return [y for y in years if y]

# Criar filme
@router.post("/", response_model=MovieResponse, status_code=201)
async def create_movie(payload: MovieCreate, db: AsyncSession = Depends(get_async_db)):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    # Verifica duplicado
    result = await db.execute(select(Movie).filter(Movie.title.ilike(title)))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Movie already exists")

    if not OMDB_API_KEY:
        raise HTTPException(status_code=500, detail="OMDB_API_KEY not configured")

    # Busca OMDb
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get("https://www.omdbapi.com/", params={"t": title, "apikey": OMDB_API_KEY})
        data = response.json()
        if data.get("Response") == "False":
            raise HTTPException(status_code=404, detail=data.get("Error", "Movie not found"))

    movie = Movie(
        title=data.get("Title") or title,
        year=data.get("Year") or "",
        director=data.get("Director") or "",
        plot=data.get("Plot") or "",
        imdb_rating=data.get("imdbRating") or "",
        poster=data.get("Poster") or "",
    )

    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie

# Listar filmes com filtros, ordenação e paginação
@router.get("/", response_model=list[MovieResponse])
async def list_movies(
    search: str = Query("", alias="search"),
    year: str = Query("All", alias="year"),
    sort_by: str = Query("title", alias="sort_by"),
    order: str = Query("asc", alias="order"),
    page: int = Query(1, alias="page"),
    limit: int = Query(6, alias="limit"),
    db: AsyncSession = Depends(get_async_db)
):
    query = select(Movie)

    if search:
        query = query.where(Movie.title.ilike(f"%{search}%"))

    if year != "All":
        query = query.where(Movie.year == year)

    if sort_by == "imdb_rating":
        if order == "asc":
            query = query.order_by(cast(Movie.imdb_rating, Float).asc())
        else:
            query = query.order_by(cast(Movie.imdb_rating, Float).desc())
    else:
        if order == "asc":
            query = query.order_by(Movie.title.asc())
        else:
            query = query.order_by(Movie.title.desc())

    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    movies = result.scalars().all()
    return movies

# Busca filme por ID
@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Movie).filter(Movie.id == movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# Deleta filme
@router.delete("/{movie_id}")
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Movie).filter(Movie.id == movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    await db.delete(movie)
    await db.commit()
    return {"message": f"Movie '{movie.title}' deleted successfully"}
