import io
import uuid
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.tasks import TaskRepository
from app.exceptions import TaskNotFound
from app.auth import get_current_user
import app.minio_client as minio

router = APIRouter(prefix="/v1/tasks", tags=["Upload"])


@router.post("/{task_id}/upload-avatar", dependencies=[Depends(get_current_user)])
async def upload_avatar(task_id: int, file: UploadFile, db: AsyncSession = Depends(get_db)):
    task = await TaskRepository(db).get_by_id(task_id)
    if not task:
        raise TaskNotFound(task_id)

    data = await file.read()
    object_name = f"{task_id}/{uuid.uuid4()}_{file.filename}"
    url = await minio.upload_file(object_name, io.BytesIO(data), len(data), file.content_type)
    return {"url": url}
