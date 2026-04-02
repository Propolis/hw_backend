from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Comment


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, text: str, task_id: int) -> Comment:
        comment = Comment(text=text, task_id=task_id)
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def get_by_task(self, task_id: int) -> list[Comment]:
        result = await self.db.execute(select(Comment).where(Comment.task_id == task_id))
        return result.scalars().all()

    async def get_by_id(self, comment_id: int) -> Comment | None:
        result = await self.db.execute(select(Comment).where(Comment.id == comment_id))
        return result.scalar_one_or_none()
