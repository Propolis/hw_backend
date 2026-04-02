from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, title: str, description: str | None, completed: bool) -> Task:
        task = Task(title=title, description=description, completed=completed)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_all(self) -> list[Task]:
        result = await self.db.execute(select(Task))
        return result.scalars().all()

    async def get_by_id(self, task_id: int) -> Task | None:
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def update(self, task: Task, update_data: dict) -> Task:
        for key, value in update_data.items():
            setattr(task, key, value)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete(self, task: Task):
        await self.db.delete(task)
        await self.db.commit()
