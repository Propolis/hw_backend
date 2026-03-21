from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services import tasks as task_service
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, dependencies=[Depends(get_current_user)])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(task, db)


@router.get("/", response_model=list[TaskResponse], dependencies=[Depends(get_current_user)])
def get_tasks(db: Session = Depends(get_db)):
    return task_service.get_all_tasks(db)


@router.get("/{task_id}", response_model=TaskResponse, dependencies=[Depends(get_current_user)])
def get_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task(task_id, db)


@router.put("/{task_id}", response_model=TaskResponse, dependencies=[Depends(get_current_user)])
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task(task_id, task, db)


@router.delete("/{task_id}", dependencies=[Depends(get_current_user)])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.delete_task(task_id, db)
