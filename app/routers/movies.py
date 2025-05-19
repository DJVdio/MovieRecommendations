from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from ..database import get_db
from app.services.douban import fetch_top250, fetch_one_week

router = APIRouter(prefix="/movies", tags=["movies"])

async def create_or_update(model, data, db):
    existing = await db.execute(
        model.__table__.select().where(model.rank == data["rank"])
    )
    if existing.scalar():
        await db.execute(
            model.__table__.update()
            .where(model.rank == data["rank"])
            .values(**data)
        )
    else:
        db.add(model(**data))
    await db.commit()

@router.post("/crawl/top250")
async def crawl_top250(db: AsyncSession = Depends(get_db)):
    try:
        movies = await fetch_top250()
        for data in movies:
            await create_or_update(models.DoubanTop250, data, db)
        return {"message": f"成功存储/更新 {len(movies)} 条TOP250数据"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/crawl/one_week")
async def crawl_one_week(db: AsyncSession = Depends(get_db)):
    try:
        movies = await fetch_one_week()
        for data in movies:
            await create_or_update(models.DoubanOneWeek, data, db)
        return {"message": f"成功存储/更新 {len(movies)} 条一周口碑数据"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top250/set_is_watched")
async def update_top250_watch_status(
    id: int,
    is_watched: bool,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.DoubanTop250).where(models.DoubanTop250.id == id)
    )
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.is_watched = is_watched
    await db.commit()
    return {"message": "Top250 movie watch status updated"}

@router.get("/one_week/set_is_watched")
async def update_one_week_watch_status(
    id: int,
    is_watched: bool,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.DoubanOneWeek).where(models.DoubanOneWeek.id == id)
    )
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.is_watched = is_watched
    await db.commit()
    return {"message": "One-week movie watch status updated"}