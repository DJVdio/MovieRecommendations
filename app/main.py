# File: main.py（保持不变）
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import movies, recommend
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(movies.router)
app.include_router(recommend.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)