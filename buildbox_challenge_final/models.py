from sqlalchemy import Column, Integer, String
from .database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    year = Column(String)
    director = Column(String)
    plot = Column(String)
    imdb_rating = Column(String)
    poster = Column(String, default="")
