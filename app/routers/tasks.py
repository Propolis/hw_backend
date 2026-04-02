from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.services.tasks import TaskService
from app.repositories.tasks import TaskRepository
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(TaskRepository(db))


@router.post("/", response_model=TaskResponse, dependencies=[Depends(get_current_user)])
async def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)):
    return await service.create_task(task)


@router.get("/", response_model=list[TaskResponse], dependencies=[Depends(get_current_user)])
async def get_tasks(service: TaskService = Depends(get_task_service)):
    return await service.get_all_tasks()


@router.get("/{task_id}", response_model=TaskResponse, dependencies=[Depends(get_current_user)])
async def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return await service.get_task(task_id)


@router.put("/{task_id}", response_model=TaskResponse, dependencies=[Depends(get_current_user)])
async def update_task(task_id: int, task: TaskUpdate, service: TaskService = Depends(get_task_service)):
    return await service.update_task(task_id, task)


@router.delete("/{task_id}", dependencies=[Depends(get_current_user)])
async def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return await service.delete_task(task_id)
