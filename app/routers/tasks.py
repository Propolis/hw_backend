from fastapi import APIRouter
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services import tasks as task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate):
    return task_service.create_task(task)


@router.get("/", response_model=list[TaskResponse])
def get_tasks():
    return task_service.get_all_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    return task_service.get_task(task_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):
    return task_service.update_task(task_id, task)


@router.delete("/{task_id}")
def delete_task(task_id: int):
    return task_service.delete_task(task_id)
