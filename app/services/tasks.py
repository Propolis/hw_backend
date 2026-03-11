from fastapi import HTTPException
from app.schemas import TaskCreate, TaskUpdate

db: dict[int, dict] = {}


def create_task(task: TaskCreate) -> dict:
    task_data = task.model_dump()
    new_id = max(db.keys(), default=0) + 1
    task_data["id"] = new_id
    db[new_id] = task_data
    return task_data


def get_all_tasks() -> list[dict]:
    return list(db.values())


def get_task(task_id: int) -> dict:
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    return db[task_id]


def update_task(task_id: int, task: TaskUpdate) -> dict:
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Not found")

    existing_task = db[task_id]
    update_data = task.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        existing_task[key] = value

    return existing_task


def delete_task(task_id: int) -> dict:
    if task_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    del db[task_id]
    return {"detail": "Deleted"}
