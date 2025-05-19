from sqlalchemy import select
from typing import Dict, Any, List, Union
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import DoubanTop250, DoubanOneWeek

async def get_all_movies(db: AsyncSession, params: Dict[str, Any]) -> List[Union[DoubanTop250, DoubanOneWeek]]:
    movies = []
    # TOP250
    if params.get("target", "both") in ["top250", "both"]:
        stmt = select(DoubanTop250).where(*(build_conditions(DoubanTop250, params)))
        movies += (await db.execute(stmt)).scalars().all()
    # One Week
    if params.get("target", "both") in ["one_week", "both"]:
        stmt = select(DoubanOneWeek).where(*(build_conditions(DoubanOneWeek, params)))
        movies += (await db.execute(stmt)).scalars().all()
    return movies


def build_conditions(model, params: Dict[str, Any]):
    conditions = []
    if "is_watched" in params:
        conditions.append(model.is_watched == params["is_watched"])
    if params.get("min_rating") is not None:
        conditions.append(model.rating >= params["min_rating"])
    return conditions