from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session
from app.repositories.task import TaskRepository
from app.schemas.task import TaskShema, TaskCreateShema, TaskUpdateShema


class TaskNotFound(Exception):
    """Задача не найдена в БД"""


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskShema]:
        tasks_orm = self.task_repository.get_all()
        #return [TaskShema(id=task.id, text=task.text, status=task.status) for task in tasks_orm]
        return [TaskShema.model_validate(task) for task in tasks_orm]

    def create_task(self, task_create: TaskCreateShema) -> TaskShema:
        tasks_orm = self.task_repository.create(text=task_create.text)
        self.db.commit()
        return TaskShema.model_validate(tasks_orm)

    def update_task(self, task_id: str, task_update: TaskUpdateShema) -> TaskShema:
        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f"Задача с id={task_id} не найдена")
        if task_update.text:
            task_for_update.text = task_update.text
        if task_update.status is not None:
            task_for_update.status = task_update.status

        self.db.commit()
        return TaskShema.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        task_for_delete = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Задача с id={task_id} не найдена")
        self.task_repository.delete(task_for_delete)
        self.db.commit()