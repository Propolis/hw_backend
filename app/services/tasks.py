from app.schemas import TaskCreate, TaskUpdate
from app.repositories.tasks import TaskRepository
from app.exceptions import TaskNotFound


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, task: TaskCreate):
        return await self.repository.create(task.title, task.description, task.completed)

    async def get_all_tasks(self):
        return await self.repository.get_all()

    async def get_task(self, task_id: int):
        task = await self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound(task_id)
        return task

    async def update_task(self, task_id: int, task: TaskUpdate):
        existing = await self.repository.get_by_id(task_id)
        if not existing:
            raise TaskNotFound(task_id)
        return await self.repository.update(existing, task.model_dump(exclude_unset=True))

    async def delete_task(self, task_id: int) -> dict:
        task = await self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound(task_id)
        await self.repository.delete(task)
        return {"detail": "Удалено"}
