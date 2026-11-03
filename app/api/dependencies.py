
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.task import TaskService


def get_task_services(db: Session=Depends(get_db)):
    """Функция для инъекции зависимости TaskService"""
    return TaskService(db)
