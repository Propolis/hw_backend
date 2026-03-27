from sqlalchemy.orm import Session
from app.models import Comment


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, text: str, task_id: int) -> Comment:
        comment = Comment(text=text, task_id=task_id)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_by_task(self, task_id: int) -> list[Comment]:
        return self.db.query(Comment).filter(Comment.task_id == task_id).all()

    def get_by_id(self, comment_id: int) -> Comment | None:
        return self.db.query(Comment).filter(Comment.id == comment_id).first()
