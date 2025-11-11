from pydantic import BaseModel
from typing import Optional

class MovieCreate(BaseModel):
    title: str

class MovieResponse(BaseModel):
    id: int
    title: str
    year: Optional[str] = None
    director: Optional[str] = None
    plot: Optional[str] = None
    imdb_rating: Optional[str] = None
    poster: str

    class Config:
        orm_mode = True
