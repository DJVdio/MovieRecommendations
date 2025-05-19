from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    rating: float
    rank: int
    is_watched: int

class DoubanTop250Create(MovieBase):
    director: str | None = None
    actors: str | None = None
    introduction: str | None = None

class DoubanOneWeekCreate(MovieBase):
    release_date: str | None = None
    actors: str | None = None
    introduction: str | None = None

class MovieResponse(MovieBase):
    id: int
    class Config:
        from_attributes = True