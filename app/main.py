import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers import tasks, auth
from app.routers import comments, upload
from app.database import engine, Base, get_db
from app.exceptions import TaskNotFound, CommentNotFound
import app.minio_client as minio


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        await minio.ensure_bucket()
    except Exception:
        pass
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(comments.router)
app.include_router(upload.router)


@app.exception_handler(TaskNotFound)
async def task_not_found_handler(request: Request, exc: TaskNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "TASK_NOT_FOUND", "message": f"Задача {exc.task_id} не найдена"}},
    )


@app.exception_handler(CommentNotFound)
async def comment_not_found_handler(request: Request, exc: CommentNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "COMMENT_NOT_FOUND", "message": f"Комментарий {exc.comment_id} не найден"}},
    )


@app.get("/health", tags=["System"])
async def health(db: AsyncSession = Depends(get_db)):
    db_ok = False
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    minio_ok = await minio.check_connection()

    return {
        "db": "ok" if db_ok else "error",
        "minio": "ok" if minio_ok else "error",
    }


@app.get("/info", tags=["System"])
async def info():
    return {
        "version": "1.0.0",
        "environment": os.getenv("ENV", "dev"),
    }
