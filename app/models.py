from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from .database import Base


class DoubanTop250(Base):
    __tablename__ = "top250"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    rating = Column(Float, nullable=False)
    director = Column(String(100))
    actors = Column(String(200))
    introduction = Column(Text)
    rank = Column(Integer, unique=True)
    is_watched = Column(Boolean, default=False)


class DoubanOneWeek(Base):
    __tablename__ = "one_week"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    rating = Column(Float, nullable=False)
    release_date = Column(String(50))
    actors = Column(String(200))
    introduction = Column(Text)
    rank = Column(Integer, unique=True)
    is_watched = Column(Boolean, default=False)