from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import tasks, auth
from app.routers import comments
from app.database import engine
from app import models
from app.exceptions import TaskNotFound, CommentNotFound

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.router)
app.include_router(auth.router)
app.include_router(comments.router)


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
