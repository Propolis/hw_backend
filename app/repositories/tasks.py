from sqlalchemy.orm import Session
from app.models import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, title: str, description: str | None, completed: bool):
        task = Task(title=title, description=description, completed=completed)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_all(self):
        return self.db.query(Task).all()

    def get_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()

    def update(self, task: Task, update_data: dict):
        if "title" in update_data:
            task.title = update_data["title"]
        if "description" in update_data:
            task.description = update_data["description"]
        if "completed" in update_data:
            task.completed = update_data["completed"]
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task):
        self.db.delete(task)
        self.db.commit()
