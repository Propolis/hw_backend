from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas import TaskCreate, TaskUpdate
from app.repositories.tasks import TaskRepository


def create_task(task: TaskCreate, db: Session):
    repository = TaskRepository(db)
    return repository.create(task.title, task.description, task.completed)


def get_all_tasks(db: Session):
    repository = TaskRepository(db)
    return repository.get_all()


def get_task(task_id: int, db: Session):
    repository = TaskRepository(db)
    task = repository.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


def update_task(task_id: int, task: TaskUpdate, db: Session):
    repository = TaskRepository(db)
    existing_task = repository.get_by_id(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    update_data = task.model_dump(exclude_unset=True)
    return repository.update(existing_task, update_data)


def delete_task(task_id: int, db: Session) -> dict:
    repository = TaskRepository(db)
    task = repository.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    repository.delete(task)
    return {"detail": "Удалено"}
