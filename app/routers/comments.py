from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import CommentCreate, CommentResponse
from app.services.comments import CommentService
from app.repositories.comments import CommentRepository
from app.repositories.tasks import TaskRepository
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/v1/tasks", tags=["Comments"])


def get_comment_service(db: AsyncSession = Depends(get_db)) -> CommentService:
    return CommentService(CommentRepository(db), TaskRepository(db))


@router.post("/{task_id}/comments", response_model=CommentResponse, dependencies=[Depends(get_current_user)])
async def create_comment(task_id: int, comment: CommentCreate, service: CommentService = Depends(get_comment_service)):
    return await service.create_comment(task_id, comment)


@router.get("/{task_id}/comments", response_model=list[CommentResponse], dependencies=[Depends(get_current_user)])
async def get_comments(task_id: int, service: CommentService = Depends(get_comment_service)):
    return await service.get_comments(task_id)
