from unittest.mock import MagicMock
from app.services.tasks import TaskService
from app.schemas import TaskCreate, TaskUpdate
from app.models import Task
from app.exceptions import TaskNotFound
import pytest


def make_task(id=1, title="Test", description=None, completed=False):
    t = Task()
    t.id = id
    t.title = title
    t.description = description
    t.completed = completed
    return t


def test_create_task():
    mock_repo = MagicMock()
    mock_repo.create.return_value = make_task(title="Test task")

    service = TaskService(mock_repo)
    result = service.create_task(TaskCreate(title="Test task"))

    mock_repo.create.assert_called_once_with("Test task", None, False)
    assert result.title == "Test task"
    assert result.completed is False


def test_create_task_with_description():
    mock_repo = MagicMock()
    mock_repo.create.return_value = make_task(title="With desc", description="desc")

    service = TaskService(mock_repo)
    result = service.create_task(TaskCreate(title="With desc", description="desc"))

    mock_repo.create.assert_called_once_with("With desc", "desc", False)
    assert result.description == "desc"


def test_get_task_not_found():
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = None

    service = TaskService(mock_repo)
    with pytest.raises(TaskNotFound) as exc_info:
        service.get_task(42)

    assert exc_info.value.task_id == 42


def test_delete_task_not_found():
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = None

    service = TaskService(mock_repo)
    with pytest.raises(TaskNotFound):
        service.delete_task(99)
