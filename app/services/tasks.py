from app.schemas import TaskCreate, TaskUpdate
from app.repositories.tasks import TaskRepository
from app.exceptions import TaskNotFound


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task: TaskCreate):
        return self.repository.create(task.title, task.description, task.completed)

    def get_all_tasks(self):
        return self.repository.get_all()

    def get_task(self, task_id: int):
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound(task_id)
        return task

    def update_task(self, task_id: int, task: TaskUpdate):
        existing = self.repository.get_by_id(task_id)
        if not existing:
            raise TaskNotFound(task_id)
        return self.repository.update(existing, task.model_dump(exclude_unset=True))

    def delete_task(self, task_id: int) -> dict:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise TaskNotFound(task_id)
        self.repository.delete(task)
        return {"detail": "Удалено"}
