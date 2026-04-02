from app.schemas import CommentCreate
from app.repositories.comments import CommentRepository
from app.repositories.tasks import TaskRepository
from app.exceptions import TaskNotFound, CommentNotFound


class CommentService:
    def __init__(self, comment_repository: CommentRepository, task_repository: TaskRepository):
        self.comment_repository = comment_repository
        self.task_repository = task_repository

    async def create_comment(self, task_id: int, comment: CommentCreate):
        if not await self.task_repository.get_by_id(task_id):
            raise TaskNotFound(task_id)
        return await self.comment_repository.create(comment.text, task_id)

    async def get_comments(self, task_id: int):
        if not await self.task_repository.get_by_id(task_id):
            raise TaskNotFound(task_id)
        return await self.comment_repository.get_by_task(task_id)
