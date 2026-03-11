from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = None
    completed: bool | None = None


class TaskResponse(TaskBase):
    id: int
