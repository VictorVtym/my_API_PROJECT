from fastapi import APIRouter, status, Depends, HTTPException

from app.api.dependencies import get_task_services
from app.schemas.task import TaskShema, TaskCreateShema, TaskUpdateShema
from app.services.task import TaskService, TaskNotFound


router = APIRouter(prefix="/tasks")


@router.get("")
def read_tasks(task_service: TaskService = Depends(get_task_services)) -> list[TaskShema]:
    return task_service.list_tasks()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_tasks(
    payload: TaskCreateShema,
    task_service: TaskService = Depends(get_task_services)
) -> TaskShema:
    return task_service.create_task(task_create=payload)


@router.patch("/{task_id}")
def update_task(
    task_id: str,
    payload: TaskUpdateShema,
    task_service: TaskService = Depends(get_task_services)
) -> TaskShema:
    try:
        return task_service.update_task(task_id=task_id, task_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskService = Depends(get_task_services)) -> None:
    try:
        return task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
